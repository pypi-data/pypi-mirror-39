#!/user/bin/env python
"""
w7x option starter
"""
import os
import numpy as np
import sys
import unittest
import doctest
import pathlib
import argparse
import matplotlib.pyplot as plt

import tfields
import w7x


def run_doctests():
    """
    Find all doctests and execute them
    """
    this_dir = pathlib.Path(__file__).parent.resolve()
    for f in list(this_dir.glob('**/*.py')):
        doctest.testfile(str(f.resolve()),
                         module_relative=False)  # , verbose=True, optionflags=doctest.ELLIPSIS)


def load_unittests(loader=None, suite=None):
    if loader is None:
        loader = unittest.TestLoader()
    if suite is None:
        suite = unittest.TestSuite()
    parent = pathlib.Path(__file__).parent.parent
    for f in list(parent.glob('*/test*.py')):
        sys.path.insert(0, str(f.parent))
        mod = __import__(f.name[:-3])
        for test in loader.loadTestsFromModule(mod):
            suite.addTests(test)
        sys.path.remove(str(f.parent))
    return suite


def run_unittests(arg):
    run_doctests()
    # unittest.main(defaultTest='load_unittests')


def diffuse(args):
    """
    diffuse a extended vmec run and save the result
    """
    raise NotImplementedError("Paths should be set by user.")
    localDir = tfields.lib.in_out.resolve("~/Data/EXTENDER/{args.vmec_id}/".format(**locals()))
    datPath = os.path.join(localDir, "{args.vmec_id}.dat".format(**locals()))

    cyl = w7x.extender.getHybridFromDat(datPath)
    grid = w7x.flt.Grid(cylinder=cyl)
    config = w7x.flt.MagneticConfig.from_dat_file(datPath, grid=grid)
    run = w7x.flt.Run(config)

    saveDir = os.path.join(args.baseDir, "{args.vmec_id}".format(**locals()))
    tfields.lib.in_out.mkdir(saveDir, isDir=True)
    path = tfields.lib.in_out.resolve(os.path.join(saveDir,
                                      '{args.vmec_id}-fld.nest.npz'.format(**locals())))
    tracerConnectionResults, componentLoads, startPoints3D = \
        run.line_diffusion(startPoints=args.startPoints)
    # npt.saveNested(path, (tracerConnectionResults, componentLoads, startPoints3D))
    """ can be read like
    tracerConnectionResults, componentLoads, startPoints3D = npt.readNested(path)
    """


def poincare(args):
    ''' poincare plot creation '''
    phiList = args.phi.values

    if args.phi.deg:
        phiList = [val / 180 * np.pi for val in phiList]

    if not args.assemblies.off:
        machine = w7x.flt.Machine.from_mm_ids(*args.assemblies.values)
    else:
        machine = w7x.flt.Machine()

    relativeCurrents = args.magneticConfig.relativeCurrents
    datPath = args.magneticConfig.path
    if datPath:
        datPath = tfields.lib.in_out.resolve(datPath)
        cyl = w7x.extender.getHybridFromDat(datPath)
        grid = w7x.flt.Grid(cylinder=cyl)
        magneticConfig = w7x.flt.MagneticConfig.from_dat_file(datPath,
                                                                 grid=grid)
    elif relativeCurrents:
        magneticConfig = w7x.flt.MagneticConfig.createWithCurrents(
            relativeCurrents=relativeCurrents)
    else:
        magneticConfig = w7x.flt.MagneticConfig.createWithCurrents()

    ''' plotting '''
    axis = tfields.plotting.gca(2)
    for phi in phiList:
        axis.grid(color='lightgrey')
        machine.plot_poincare(phi, axis=axis)
        magneticConfig.plot_poincare(phi, axis=axis)
        tfields.plotting.save("~/tmp/poincare-{phi:.4f}".format(**locals()), 'png', 'pgf', 'pdf')
        axis.clear()


def partition_divertor(args):
    """
    cluster the strikeline into the divertor tiles
    """
    from clusterDivertorPartitions import getTileLoadsFromDiffusion, plotTileLoads
    saveDir = os.path.join(args.baseDir, "{args.vmec_id}".format(**locals()))
    path = tfields.lib.in_out.resolve(os.path.join(saveDir,
                                      '{args.vmec_id}-fld.nest.npz'.format(**locals())))
    loads = getTileLoadsFromDiffusion(path)
    plotTileLoads(loads, vmin=0, vmax=60000)
    plt.show()
    


if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='W7-X tools app')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "test" command
    parserExtend = subparsers.add_parser('test', help='test help')
    parserExtend.set_defaults(func=run_unittests)

    # create the parser for the "extend" command
    parserExtend = subparsers.add_parser('extend', help='extend help')
    parserExtend.add_argument('vmec_id', type=str, help='vmec_id to extend')
    parserExtend.set_defaults(func=w7x.extender.extend)

    # create the parser for the "diffuse" command
    parserDiffuse = subparsers.add_parser('diffuse', help='diffuse help')
    parserDiffuse.add_argument('vmec_id', type=str,
                               help='already extended vmec_id')
    parserDiffuse.add_argument('--startPoints', type=int,
                               help="hit points = 2 * "
                               "startPoints (forward and backward).",
                               default=12500)
    parserDiffuse.add_argument('--baseDir', type=str,
                               default="~/Data/Strikeline/",
                               help='already extended vmec_id')
    parserDiffuse.set_defaults(func=diffuse)

    # create the parser for the "poincare" command
    parserPoincare = subparsers.add_parser('poincare', help='poincare help')
    parserPoincare.add_argument('--baseDir', type=str,
                                default="~/Data/Strikeline/",
                                help='already extended vmec_id')
    parserPoincare.add_argument('--phi', dest='phi.values', nargs='*', type=float,
                                default=[0.])
    parserPoincare.add_argument('--phi.deg', dest='phi.deg',
                                help='switch phi from radian to degree',
                                action="store_true")
    parserPoincare.add_argument('--assemblies', dest='assemblies.values',
                                nargs='+', type=str,
                                default=w7x.Defaults.Machine.mm_ids)
    parserPoincare.add_argument('--assemblies.off',
                                action="store_true")
    parserPoincare.add_argument('--magneticConfig.relativeCurrents',
                                help='relative currents in case of vacuum config')
    parserPoincare.add_argument('--magneticConfig.coilConfig',
                                help='set the coil config for the relative currents')
    parserPoincare.add_argument('--magneticConfig.path',
                                default=None,
                                help='create config with magnetic field grid at path')
    parserPoincare.set_defaults(func=poincare)

    # create the parser for the "partition_divertor" command
    parserClusterTiles = subparsers.add_parser('partition_divertor',
                                               help='partition_divertor help')
    parserClusterTiles.add_argument('vmec_id', type=str,
                                    help='already extended and diffued vmec_id')
    parserClusterTiles.add_argument('--baseDir', type=str,
                                    default="~/Data/Strikeline/",
                                    help='already extended vmec_id')
    parserClusterTiles.set_defaults(func=partition_divertor)
    
    args = parser.parse_args()
    args.func(args)
