# coding: utf-8
# Copyright (c) Seong-Gon Kim

from __future__ import division, unicode_literals

import os
import re
import itertools
import warnings
import logging
import math
import glob

import six
import numpy as np
from numpy.linalg import det
from collections import OrderedDict, namedtuple
from hashlib import md5

from monty.io import zopen
from monty.os.path import zpath
from monty.json import MontyDecoder

from enum import Enum
from tabulate import tabulate

import scipy.constants as const

from pymatgen import SETTINGS
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element, get_el_sp
from pymatgen.util.string import str_delimited
from pymatgen.util.io_utils import clean_lines
from monty.json import MSONable

from msudft.util.string import list_to_str

"""
Classes for reading/manipulating/writing XCSF files.
"""

__author__ = "Seong-Gon Kim, Mississippi State University"
__copyright__ = "Copyright 2018, Seong-Gon Kim"
__version__ = "1.0"
__maintainer__ = "Seong-Gon Kim"
__email__ = "sk162@msstate.edu"
__status__ = "Beta"
__date__ = "2018/12/03"


logger = logging.getLogger(__name__)


class XCSF(MSONable):
    """
    Object for representing the data in a XCSF file.

    Args:
        structure (Structure):  Structure object.
        name (str): Optional name for the structure. Defaults to unit
            cell formula of structure. Defaults to None.
        selective_dynamics (Nx3 array): bool values for selective dynamics,
            where N is number of sites. Defaults to None.
        velocities (Nx3 array): Velocities for the XCSF. Typically parsed
            in MD runs or can be used to initialize velocities.

    .. attribute:: structure

        Associated Structure.

    .. attribute:: name

        Optional name string.

    .. attribute:: selective_dynamics

        Selective dynamics attribute for each site if available. 
        A Nx3 array of booleans.

    .. attribute:: velocities

        Velocities for each site. A Nx3 array of floats.

    """

    def __init__(self, structure, name=None, info=None,
                 atominfo=None,
                 selective_dynamics=None,
                 velocities=None):

        site_properties = {}
        if atominfo:
            site_properties["atominfo"] = atominfo
        if selective_dynamics:
            site_properties["selective_dynamics"] = selective_dynamics
        if velocities:
            site_properties["velocities"] = velocities
        structure = Structure.from_sites(structure)
        self.structure = structure.copy(site_properties=site_properties)
        self.name = structure.formula if name is None else name
        self.info = '' if info is None else info

    @property
    def atominfo(self):
        return self.structure.site_properties.get("atominfo")

    @property
    def velocities(self):
        return self.structure.site_properties.get("velocities")

    @property
    def selective_dynamics(self):
        return self.structure.site_properties.get("selective_dynamics")

    @atominfo.setter
    def atominfo(self, atominfo):
        self.structure.add_site_property("atominfo", atominfo)

    @velocities.setter
    def velocities(self, velocities):
        self.structure.add_site_property("velocities", velocities)

    @selective_dynamics.setter
    def selective_dynamics(self, selective_dynamics):
        self.structure.add_site_property("selective_dynamics",
                                         selective_dynamics)

    @property
    def site_symbols(self):
        """
        Sequence of symbols associated with the XCSF. 
        """
        syms = [site.specie.symbol for site in self.structure]
        return [a[0] for a in itertools.groupby(syms)]

    @property
    def natoms(self):
        """
        Sequence of number of sites of each type associated with the XCSF.
        Similar to 7th line in vasp 5+ POSCAR
        """
        syms = [site.specie.symbol for site in self.structure]
        return [len(tuple(a[1])) for a in itertools.groupby(syms)]

    def __setattr__(self, name, value):
        if name in ("atominfo", "selective_dynamics", "velocities"):
            if value is not None and len(value) > 0:
                value = np.array(value)
                dim = value.shape
                if dim[1] != 3 or dim[0] != len(self.structure):
                    raise ValueError(name + " array must be same length as" +
                                     " the structure.")
                value = value.tolist()
        super(XCSF, self).__setattr__(name, value)

    @staticmethod
    def from_file(filename):
        """
        Reads a XCSF from a file.

        Args:
            filename (str): File name for the XCSF file.

        Returns:
            XCSF object.
        """
        with zopen(filename, "rt") as f:
            return XCSF.from_string(f.read())

    @staticmethod
    def from_string(data):
        """
        Reads a XCSF from a string.

        Args:
            data (str): String containing XCSF data.

        Returns:
            XCSF object.
        """
        import xml.etree.ElementTree as ET
        root = ET.fromstring(data)

        # convert the tree to a structure
        name = None
        node = root.find("name")
        if node != None:
            if node.text != None:
                name = node.text.strip()

        info = None
        node = root.find("info")
        if node != None:
            if node.text != None:
                info = node.text.strip()

        lattice = XCSF._read_lattice(root)
        atomsymbol, ifcart, atompos, atominfo = XCSF._read_atomlist(root)
        selective_dynamics = XCSF._read_selective_dynamics(root)
        velocities = XCSF._read_velocities(root)

        structure = Structure(lattice, atomsymbol, atompos,
                              to_unit_cell=False, validate_proximity=False,
                              coords_are_cartesian=ifcart)

        return XCSF(structure, name, info,
                    atominfo=atominfo,
                    selective_dynamics=selective_dynamics, 
                    velocities=velocities)

    def _read_lattice(root):
        matrix = np.eye(3)
        node = root.find('lattice')
        if node is None:
            raise Exception("<lattice> tag missing")
        for elem in node.iter():
            if elem.tag == "scale":
                svec = elem.get("vector")
                if svec == None:
                    raise Exception('%xcsf-error: "vector" is missing in <scale> tag')
                lattscale = np.array(eval(svec), dtype=float)
            if elem.tag == "axis":
                aname = elem.get("name")
                try:
                    aid = ["a1","a2","a3"].index(aname)
                except ValueError:
                    raise Exception(
                        '%xcsf-error: Invalid axis name "{}"'.format(aname))
                svec = elem.get("vector")
                if svec == None:
                    raise Exception('%xcsf-error: "vector" is missing in <axis> tag')
                avec = np.array(eval(svec), dtype=float)
                matrix[aid] = avec*lattscale[aid]
        return Lattice(matrix)

    def _read_atomlist(root):
        atomsymbol = []
        atompos = []
        atominfo = []
        node = root.find("atomlist")
        if node == None:
            raise Exception("<atomlist> tag missing")
        sname = node.get("coord")
        if sname == None:
            raise Exception('"<atomlist coord" attribute missing')
        elif sname == "cart":
            ifcart = True
        elif sname == "frac":
            ifcart = False
        else:
            raise Exception('%xcsf-error: invalid coord value "{}"'.format(coord))

        for elem in node.iter():
            if elem.tag == "atom":
                indx = len(atomsymbol)+1
                symbol = elem.get("symbol")
                if symbol == None:
                    symbol = elem.get("type", default="??")
                atomsymbol.append(symbol)
                svec = elem.get("pos")
                if svec == None:
                    raise Exception('%xcsf-error: "pos" is missing in <atom> tag')
                pos = np.array(eval(svec), dtype=float)
                atompos.append(pos)
                info = elem.get("info", default="")
                atominfo.append(info)

        return atomsymbol, ifcart, atompos, atominfo

    def _read_selective_dynamics(root):
        return None

    def _read_velocities(root):
        return None

    def get_string(self, ifcart=False, verbose=0, 
                   significant_figures=6):
        """
        Returns a string to be written as a XCSF file. 

        Args:
            ifcart (bool): Flag to write coordinates in cartesian. 
                Defaults to False.
            significant_figures (int): No. of significant figures to
                output all quantities. Defaults to 6. Note that positions are
                output in fixed point, while velocities are output in
                scientific format.

        Returns:
            String representation of XCSF.
        """

        # This corrects for VASP really annoying bug of crashing on lattices
        # which have triple product < 0. We will just invert the lattice
        # vectors.
        latt = self.structure.lattice
        if np.linalg.det(latt.matrix) < 0:
            latt = Lattice(-latt.matrix)

        format_str = "{{:.{0}f}}".format(significant_figures)

        # Header
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append['<structure>']
        lines.append['  <name>{}</name>'.format(self.name)]
        lines.append['  <info>{}</info>'.format(self.info)]
        # Lattice
        lines.append['  <lattice>']
        lines.append['    <scale vector="[1.0, 1.0, 1.0]" />']
        for (aid, avec) in enumerate(latt.matrix):
            lines.append['    <axis name="a{}" vector="{}" />'.format(
                aid+1, list_to_str(avec))]
        lines.append['  </lattice>']
        # atomlist
        if ifcart:
            s = 'cart'
        else:
            s = 'frac'
        lines.append['  <atomlist coord="{}" >\n'.format(s))
        for (i, site) in enumerate(self.structure):
            s = '    <atom id="{}"'.format(i+1)
            s += ' symbol="{}"'.format(site.species_string())
            if coord == "frac":
                pos = atom.fpos
            else:
                pos = np.dot(structure.unitcell.f2c, atom.fpos)
            s += ' pos="{}"'.format(cmptlib.list2str(pos))
            s += ' info="{}" />\n'.format(atom.info)
            lines.append[s)
        lines.append['  </atomlist>\n')
        lines.append['</structureecule>\n')



        
        lines = [self.comment, "1.0"]
        for v in latt.matrix:
            lines.append(" ".join([format_str.format(c) for c in v]))

        if self.true_names and not vasp4_compatible:
            lines.append(" ".join(self.site_symbols))
        lines.append(" ".join([str(x) for x in self.natoms]))
        if self.selective_dynamics:
            lines.append("Selective dynamics")
        lines.append("direct" if direct else "cartesian")

        for (i, site) in enumerate(self.structure):
            coords = site.frac_coords if direct else site.coords
            line = " ".join([format_str.format(c) for c in coords])
            if self.selective_dynamics is not None:
                sd = ["T" if j else "F" for j in self.selective_dynamics[i]]
                line += " %s %s %s" % (sd[0], sd[1], sd[2])
            line += " " + site.species_string
            lines.append(line)

        if self.velocities:
            try:
                lines.append("")
                for v in self.velocities:
                    lines.append(" ".join([format_str.format(i) for i in v]))
            except:
                warnings.warn("Velocities are missing or corrupted.")

        if self.predictor_corrector:
            lines.append("")
            if self.predictor_corrector_preamble:
                lines.append(self.predictor_corrector_preamble)
                pred = np.array(self.predictor_corrector)
                for col in range(3):
                    for z in pred[:,col]:
                        lines.append(" ".join([format_str.format(i) for i in z]))
            else:
                warnings.warn(
                    "Preamble information missing or corrupt. " 
                    "Writing XCSF with no predictor corrector data.")

        return "\n".join(lines) + "\n"

    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of XCSF file.
        """
        return self.get_string()

    def write_file(self, filename, **kwargs):
        """
        Writes POSCAR to a file. The supported kwargs are the same as those for
        the XCSF.get_string method and are passed through directly.
        """
        with zopen(filename, "wt") as f:
            f.write(self.get_string(**kwargs))

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "structure": self.structure.as_dict(),
                "selective_dynamics": np.array(
                    self.selective_dynamics).tolist(),
                "velocities": self.velocities,
                "name": self.name}

    @classmethod
    def from_dict(cls, d):
        return XCSF(Structure.from_dict(d["structure"]),
                    comment=d["comment"],
                    selective_dynamics=d["selective_dynamics"],
                    velocities=d.get("velocities", None))

    def set_temperature(self, temperature):
        """
        Initializes the velocities based on Maxwell-Boltzmann distribution.
        Removes linear, but not angular drift (same as VASP)

        Scales the energies to the exact temperature (microcanonical ensemble)
        Velocities are given in A/fs. This is the vasp default when
        direct/cartesian is not specified (even when positions are given in
        direct coordinates)

        Overwrites imported velocities, if any.

        Args:
            temperature (float): Temperature in Kelvin.
        """
        # mean 0 variance 1
        velocities = np.random.randn(len(self.structure), 3)

        # in AMU, (N,1) array
        atomic_masses = np.array([site.specie.atomic_mass.to("kg")
                                  for site in self.structure])
        dof = 3 * len(self.structure) - 3

        # scale velocities due to atomic masses
        # mean 0 std proportional to sqrt(1/m)
        velocities /= atomic_masses[:, np.newaxis] ** (1 / 2)

        # remove linear drift (net momentum)
        velocities -= np.average(atomic_masses[:, np.newaxis] * velocities,
                                 axis=0) / np.average(atomic_masses)

        # scale velocities to get correct temperature
        energy = np.sum(1 / 2 * atomic_masses *
                        np.sum(velocities ** 2, axis=1))
        scale = (temperature * dof / (2 * energy / const.k)) ** (1 / 2)

        velocities *= scale * 1e-5  # these are in A/fs

        self.temperature = temperature
        try:
            del self.structure.site_properties["selective_dynamics"]
        except KeyError:
            pass

        try:
            del self.structure.site_properties["predictor_corrector"]
        except KeyError:
            pass
        # returns as a list of lists to be consistent with the other
        # initializations

        self.structure.add_site_property("velocities", velocities.tolist())

