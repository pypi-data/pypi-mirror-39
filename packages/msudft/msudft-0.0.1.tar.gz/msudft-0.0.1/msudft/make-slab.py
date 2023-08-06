#!/usr/bin/env python
"""
make-slab: Make a slab from given structure
"""

import pymatgen as mg
import math
import numpy as np
import msudft

class makeSlab:

    def __init__(self):

        pass

    def run(self, args):

        # banner
        print('===================')
        print('   MAKE SLAB   ')
        print('===================')

        # read input file
        from pymatgen.io.vasp import Poscar
        poscar0 = Poscar.from_file(args.infile)
        str0 = poscar0.structure
        print()
        print('=======  Input structure  ============')
        print(str0)

        # Slab generator
        from pymatgen.core.surface import SlabGenerator
        gen = SlabGenerator(initial_structure=str0,
                             miller_index=args.miller_index,
                             min_slab_size=args.min_slab_size,
                             min_vacuum_size=args.min_vac_size,
                             in_unit_planes=args.in_unit_planes
        )
        slab = gen.get_slab()
        print(slab)

        # write output file
        poscar1 = Poscar(slab)
        comment = "slab " + args.infile + " " + str(args.miller_index)
        poscar1.comment = comment
        poscar1.write_file(filename=args.outfile, direct=False)

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='Make a slab from a given input structure')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile',
                        help='Input structure file')
    parser.add_argument('outfile',
                        help='Output structure file for the slab')
    parser.add_argument('miller_index', type=str,
                        help='Miller index of plane parallel to surface, Ex) "[0,0,1]"')
    parser.add_argument('min_slab_size', type=float,
                        help='Minimum size of layers containing atoms')
    parser.add_argument('min_vac_size', type=float,
                        help='Minimize size of vacuum')
    parser.add_argument('--in_unit_planes', action='store_true',
                        help='Flag to set min_slab_size and min_vac_size in units of hkl planes. If not set, Ang is used.')

    args = parser.parse_args()
    print(args)
    # convert miller index
    try:
        index = eval(args.miller_index)
        args.miller_index = index
    except IOError:
        print('Invalid Miller index')
        raise

    app = makeSlab()
    app.run(args)
