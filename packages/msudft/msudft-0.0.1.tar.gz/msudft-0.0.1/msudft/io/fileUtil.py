#!/usr/bin/env python
"""
Module for file I/O
"""

import pymatgen as mg
from pymatgen.io.vasp import Poscar
import os
from msudft.io import xcsf

def read(infile, fmt=None, option=None, reportlevel=0):
    """
    Read a structure from an input file "infile"
    """
    # open input file
    try:
        f = open(infile, 'r')
        print('%fileUtil.read: Reading input file "{}"'.format(infile))
    except IOError:
        util.Error('%fileUtil.read: Failed to open input file "{}"'.format(infile))

    if fmt == None:
        fmt = os.path.splitext(infile)[1][1:]
    if reportlevel > 3:
        print('%fileUtil.read: input format =', fmt)

    if fmt == "xcsf":
        structure = xcsf.XCSF.from_file(infile).structure
    elif fmt == "vasp" or fmt == "poscar":
        structure = Poscar.from_file(infile).structure
    elif fmt == "pdb":
        mol = pdb.read(f, reportlevel)
    elif fmt == "fdf":
        mol = fdf.read(f, reportlevel)
    elif fmt == "xsf":
        mol = xsf.read(f, reportlevel)
    elif fmt == "xyz":
        mol = xyz.read(f, reportlevel)
    else:
        util.Error('%fileUtil.read: Unrecognized format "{}"'.format(fmt))

    return structure

def write(structure, outfile, fmt=None, coord=None,
          option=None, reportlevel=0):
    """
    Write a structure to an output file
    """
    # open output file
    try:
        f = open(outfile, 'w')
        print('%fileUtil.write: Writing output file "{}"'.format(outfile))
    except IOError:
        util.Error('%fileUtil.write: Failed to open output file "{}"'.format(outfile))

    if fmt == None:
        fmt = os.path.splitext(outfile)[1][1:]
    if reportlevel > 3:
        print('%fileUtil.write: output format =', fmt)

    if fmt == "xcsf":
        xcsf.XCSF(structure).write_file(outfile,
                                        coord=coord,
                                        reportlevel=reportlevel)
    elif fmt == "fdf":
        fdf.write(mol, f, coord, reportlevel)
    elif fmt == "pdb":
        pdb.write(mol, f, reportlevel)
    elif fmt == "vasp" or fmt == "poscar":
        if coord == None:
            frac = True
        elif coord == 'frac':
            frac = True
        else:
            frac = False
        str1 = structure.get_sorted_structure()
        Poscar(str1).write_file(outfile, direct=frac)
    elif fmt == "xsf":
        xsf.write(mol, f, reportlevel)
    else:
        util.Error('%fileUtil.write: Unrecognized format "{}"'.format(fmt))

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='fileUtil: Molecule file IO utility')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')

    args = parser.parse_args()

    mol = read(args.infile, args.reportlevel)
    write(mol, args.outfile, args.reportlevel)
