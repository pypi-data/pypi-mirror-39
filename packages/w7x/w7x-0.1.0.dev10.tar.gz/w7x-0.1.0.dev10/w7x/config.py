import os
import numpy as np
import tfields
from w7x import GeoSet


class Server:
    addr_field_line_server = "http://esb:8280/services/FieldLineProxy?wsdl"  # cluster alle esb
    # addr_mesh_server = "http://esb.ipp-hgw.mpg.de:8280/services/MeshSrv?wsdl"
    # addr_mesh_server = "http://lxpowerboz.ipp-hgw.mpg.de:88/services/cpp/MeshSrv?wsdl"
    # addr_mesh_server = "http://lxpowerboz:88/services/cpp/MeshSrv?wsdl"
    addr_mesh_server = "http://esb.ipp-hgw.mpg.de:8280/services/MeshSrv?wsdl"
    addr_vmec_server = "http://esb.ipp-hgw.mpg.de:8280/services/vmec_v8?wsdl"
    addr_extender_server = "http://esb.ipp-hgw.mpg.de:8280/services/Extender?wsdl"
    addr_components_db = "http://esb.ipp-hgw.mpg.de:8280/services/ComponentsDBProxy?wsdl"
    addr_coils_db = "http://esb.ipp-hgw.mpg.de:8280/services/CoilsDBProxy?wsdl"


class Coils:
    # ideal coils ids
    idealNonPlanarCoilIds = list(range(160, 210))  # non planar coils (5 each half module)
    idealPlanarCoilIds = list(range(210, 230))  # planar A and B for all 10 half modules
    idealSweepCoilIds = list(range(230, 240))  # sweep coils for all 10 half modules
    idealTrimCoilIds = [350, 241, 351, 352, 353]  # trim coils in modules 1, 2, 3, 4, 5
    idealCoilIds = idealNonPlanarCoilIds + idealPlanarCoilIds + idealSweepCoilIds

    # ideal deformed coils. They fit best to M. Otte fluxsurface measurements in op11 for highIota and jConfig. Half of the planed current is used here.
    deformedNonPlanarCoilIds = list(range(1012, 1062))
    deformedPlanarCoilIds = list(range(1062, 1082))
    deformedCoilIds = deformedNonPlanarCoilIds + deformedPlanarCoilIds + idealSweepCoilIds  # No Sweep coils provided here!

    # coils calculated by T. Andreva. Asbuilt with deformations
    asbuiltNonPlanarCoilIds = list(range(1152, 1202))
    asbuiltPlanarCoilIds = list(range(1202, 1222))
    asbuiltCoilIds = deformedNonPlanarCoilIds + deformedPlanarCoilIds + idealSweepCoilIds  # No Sweep coils provided here!


class MeshedModelsIds(object):
    meshEnd = GeoSet([164], "meshEnd", 'black')
    divertor = GeoSet([165, 166, 167, 168, 169], "divertor", 'firebrick')
    divertorKisslingerSagged = GeoSet(range(50, 60), "Sagged")
    divertorKisslinger = GeoSet(range(30, 70), "divertorKisslinger")
    # Top and bottom baffles
    baffle = GeoSet([320, 321, 322, 323, 324], "baffle", 'black')
    #  Top and bottom toroidal closures
    tda = GeoSet([325, 326, 327, 328, 329], "tda", 'dimgrey')
    # Heat shield - wall protection with carbon tiles
    shield = GeoSet([330, 331, 332, 333, 334], "shield", 'slategrey')
    # Steel panels - wall protection with stainless steel
    panel = GeoSet([335, 336, 337, 338, 339], "panel", 'grey')
    # Inner plasma vessel
    vessel = GeoSet([340, 341, 342, 343, 344], "vessel", 'dimgrey')
    scraper = GeoSet([349, 350, 351, 352, 353, 354, 355, 356, 357, 358],
                     "scraper", 'darkslateblue')
    # limiters as used in the mapping for ir. Closest to op1.1
    limiterOP11 = GeoSet([489, 488, 487, 486, 485], "limiterOP11", 'firebrick')
    # EPS2014 here the tiles are not existing. one greate plane
    limiter = GeoSet([479, 480, 481, 482, 483], "limiter", 'firebrick')


class Defaults:
    fieldSymmetry = 5

    class VMEC:
        maxIterationsPerSequence = 8000
        maxToroidalMagneticFlux = -2.64726e00
        timeStep = 0.6
        numGridPointsRadial = [4, 9, 28, 99]
        forceToleranceLevels = [1e-3, 1e-5, 1e-9, 1e-14]
        totalToroidalCurrent = 0.0

    class CartesianGrid:
        numX = 500
        numY = 500
        numZ = 100
        ZMin = -1.5
        ZMax = 1.5
        XMin = -7
        XMax = 7
        YMin = -7
        YMax = 7

    class CylindricalGrid:
        RMin = 4.05
        RMax = 6.75
        ZMin = -1.35
        ZMax = 1.35
        numR = 181
        numZ = 181
        numPhi = 96 * 5 + 1
        PhiMin = None
        PhiMax = None

    class MagneticConfig:
        standard_rw = [1., 1., 1., 1., 1., 0., 0., 0., 0.]
        high_iota_rw = [1., 1., 1., 1., 1., -0.23, -0.23, 0., 0.]
        low_iota_rw = [1., 1., 1., 1., 1., 0.25, 0.25, 0., 0.]
        inward_shifted_rw = [1., 1., 1., 1., 1., 0.1, -0.2, 0., 0.]
        outward_shifted_rw = [1., 1., 1., 1., 1., -0.14, 0.14, 0., 0.]
        high_iota_a_rw = [1., 1., 1., 1., 1., -0.25, 0., 0., 0.]
        high_iota_b_rw = [1., 1., 1., 1., 1., 0., -0.25, 0., 0.]
        low_iota_a_rw = [1., 1., 1., 1., 1., 0.25, 0., 0., 0.]
        low_iota_b_rw = [1., 1., 1., 1., 1., 0., 0.25, 0., 0.]

        default_currents_rw = standard_rw
        scale = 1.43e6
        coilsIds = Coils.idealCoilIds
        n_windigs_npcs = 108
        n_windigs_plcs = 36
        n_windigs_scs = 8

    class Machine:
        mm_ids = ['divertor', 'baffle', 'tda', 'shield', 'panel', 'vessel']

    class Poincare:
        stepSize = 10e-3
        nPoints = 300
        seeds = tfields.Points3D(np.full((40, 3), 0.),
                                 coord_sys=tfields.bases.CYLINDER)
        seeds[:20, 0] = np.linspace(5.95, 6.28, 20)
        seeds[20:25, 0] = np.linspace(5.43, 5.63, 5)
        seeds[25:30, 0] = np.linspace(5.43, 5.63, 5)
        seeds[30:35, 0] = np.linspace(5.40, 5.52, 5)
        seeds[35:40, 0] = np.linspace(5.40, 5.52, 5)
        seeds[:20, 2] = np.linspace(0.0, 0.0, 20)
        seeds[20:25, 2] = np.linspace(0.94, 0.94, 5)
        seeds[25:30, 2] = np.linspace(-0.94, -0.94, 5)
        seeds[30:35, 2] = np.linspace(0.85, 0.60, 5)
        seeds[35:40, 2] = np.linspace(-0.85, -0.60, 5)

        geometry_color = 'grey'

    class Diffusion:
        diffusion = 1.0  # [m^2/s]
        velocity = 140000  # [m/s] (10 - 200 eV  -> 140000 m/s)
        meanFreePath = 0.1  # [m]
        stepSize = 5e-2  # [m]
        nRevolutions = 4000
        startPointShift = 0.

    class Overload:
        maxLoadPumpingGapStirn = 2  # MW/m^2
        maxLoadPumpingGapDach = 5  # MW/m^2
        maxLoadCooled = 10  # MW/m^2
        maxLoadSagged = 1  # MW/m^2
        maxPeakLoads = {}  # Other Components Max loads in MW/m^2
        maxPeakLoads['baffle'] = 0.5
        maxPeakLoads['tda'] = 0.5
        maxPeakLoads['shield'] = 0.5  # only in higher loaded area, elsewhere 0.3
        maxPeakLoads['panel'] = 0.2
        maxPeakLoads['vessel'] = 0.0019
        radius = 0.022

    class Paths:
        """
        VMEC + EXTENDER standard case (0 current, 0 pressure):
        field_mfbe181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.dboe_01.v_00_pres_00_it_12.dat
        """
        divertor_upper_tiles_template_path = os.path.join(os.path.dirname(__file__),
                                                          'data/cut_templates/mm_id-165-upper-tiles/')
        baffle_upper_tiles_template_path = os.path.join(os.path.dirname(__file__),
                                                        'data/cut_templates/mm_id-320-upper-tiles/')
        shield_upper_tiles_template_path = os.path.join(os.path.dirname(__file__),
                                                        'data/cut_templates/mm_id-330-upper-tiles/')
        test_dat_file = os.path.join(os.path.dirname(__file__),
                                   'data/test.dat')
        afsExchDir = '/afs/ipp-garching.mpg.de/u/dboe/exch'
        extenderDataPath = os.path.join("~/Data/", "EXTENDER")
