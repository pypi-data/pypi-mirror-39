"""
vmec tools revolving around the Run class
"""
import copy
import json
import os
import numpy as np
import time
import logging
import warnings
import pathlib
import tfields
import sympy
from symfit import Variable, Fit, Model, parameters, variables
import w7x
import transcoding as tc
input_transcoding = w7x.transcodings.vmec_input.get_transcoding()
threed1_transcoding = w7x.transcodings.vmec_threed1.get_transcoding()


class TooLongError(ValueError):
    pass


THISDIR = pathlib.Path(__file__).resolve()


def fit(fun, x, y):
    """
    Fit a sympy function fun with data x, y
    """
    f = Variable("f")
    model = Model({f: fun})
    fit = Fit(model, x, y)
    res = fit.execute()
    fun = model[f]
    for p in res.params:
        fun = fun.subs(p, res.params.get_value(p))
    return fun


def pad(seq, target_length, padding=None):
    """
    Extend the sequence seq with padding (default: None) so as to make
    its length up to target_length. Return copy of seq. If seq is already
    longer than target_length, raise TooLongError.

    Examples:
        >>> from w7x.vmec import pad
        >>> pad([], 5, 1)
        [1, 1, 1, 1, 1]
        >>> pad([1, 2, 3], 7)
        [1, 2, 3, None, None, None, None]
        >>> pad([1, 2, 3], 2)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        TooLongError: sequence too long (3) for target length 2

    """
    seq = seq[:]
    length = len(seq)
    if length > target_length:
        raise TooLongError("sequence too long ({}) for target length {}"
                           .format(length, target_length))
    seq.extend([padding] * (target_length - length))
    return seq


class Points3D(w7x.flt.Points3D):
    ws_server = w7x.Server.addr_vmec_server


class VMECBase(w7x.core.Base):
    ws_server = w7x.Server.addr_vmec_server


class Profile(VMECBase):
    prop_defaults = {
        'ProfileType': None,
        'coefficients': []
    }

    ws_class = "Profile"

    def __init__(self, *args, **kwargs):
        '''Remove 0s from coefficients'''
        if 'coefficients' in kwargs:
            while True:
                if len(kwargs['coefficients']) == 0:
                    break
                if kwargs['coefficients'][-1] != 0:
                    break
                kwargs['coefficients'].pop(-1)
        super(Profile, self).__init__(*args, **kwargs)

    def __call__(self, value):
        raise NotImplementedError("A Profile must implement the __call__"
                                  "function")

    def normalized(self):
        raise NotImplementedError("A Profile must implement the normalized"
                                  "function")

    def scale(self, scale):
        self.coefficients = [c * scale for c in self.coefficients]

    def deviation(self, other):
        """
        Returns the normalized deviation of the profiles.
        """
        if self.ProfileType != other.ProfileType:
            return np.inf
        l = max(len(self.coefficients), len(other.coefficients))
        dev = np.sqrt(float(sum(map(lambda x: (x[0] - x[1])**2,
                                    zip(pad(self.normalized(), l, padding=0),
                                        pad(other.normalized(), l, padding=0))))))
        return dev

    def plot(self, **kwargs):
        raise NotImplementedError("A Profile must implement the plot function")


class PowerSeries(Profile):
    """
    Examples:
        >>> import w7x
        >>> default_pressure_profile = w7x.vmec.PowerSeries()

    """
    prop_defaults = Profile.prop_defaults
    prop_defaults['ProfileType'] = 'power_series'
    prop_defaults['coefficients'] = [1e-6, -1e-6]

    @property
    def norm(self):
        """
        the first coefficient
        """
        if len(self.coefficients) == 0:
            return 0
        return self.coefficients[0]

    @norm.setter
    def norm(self, norm):
        self.coefficients = [norm * x for x in self.normalized()]

    def normalized(self):
        """
        Returns:
            normalized coefficients
        """
        if len(self.coefficients) == 0:
            return []
        if self.norm == 0:
            if any([c != 0 for c in self.coefficients]):
                raise ValueError("Norm is 0")
            return [0. for x in self.coefficients]
        return [x * 1. / self.norm for x in self.coefficients]

    def __call__(self, value):
        poly = np.polynomial.polynomial.Polynomial(self.coefficients)
        return poly.__call__(value)

    def plot(self, **kwargs):
        tfields.plotting.plot_function(self, **kwargs)


def create_profile(*args, **kwargs):
    """
    Factory method for profile creation
    """
    log = logging.getLogger()
    profileType = kwargs['ProfileType']
    if profileType == 'power_series' or 'spline' in profileType:
        return PowerSeries(*args, **kwargs)
    else:
        log.error("No Profile subclass matches type {profileType}.")
        return Profile(*args, **kwargs)


class FourierCoefficients(VMECBase):
    ws_class = "FourierCoefficients"
    prop_defaults = {
        'coefficients': None,
        'poloidalModeNumbers': None,  # m
        'toroidalModeNumbers': None,  # n
        'numRadialPoints': 0
    }

    def __init__(self, *args, **kwargs):
        super(FourierCoefficients, self).__init__(*args, **kwargs)
        # check coefficients for negative m=0,n<0 to be 0
        for i, n in enumerate(self.toroidalModeNumbers):
            # m = 0
            if n < 0:
                log = logging.getLogger()
                log.debug("For m=0, n<0 coefficients may not be != 0. "
                          "Set them to be 0.")
                if self.coefficients[i] != 0.:
                    self.coefficients[i] = 0.
            else:
                break
        nCoeffs = len(self.coefficients)
        nTor = len(self.toroidalModeNumbers)
        mPol = len(self.poloidalModeNumbers)
        if not nCoeffs == nTor * mPol:
            raise ValueError("len(coeffs)({nCoeffs}) != nTor({nTor}) *"
                             " mPol({mPol})".format(**locals()))


class SurfaceCoefficients(VMECBase):
    ws_class = "surfaceCoefficients"
    prop_defaults = {
        'RCos': None,
        'ZSin': None,
        'RSin': None,
        'ZCos': None
    }

    def __init__(self, *args, **kwargs):
        super(SurfaceCoefficients, self).__init__(*args, **kwargs)
        """
        The wsDoku says you need to define hybrid but haukes code shows cylindrical.
        I will take default hybrid grid.
        It appears to not have any effect to change between the two.
        """
        if self.RCos is None:
            self.RCos = FourierCoefficients()
        if self.ZSin is None:
            self.ZSin = FourierCoefficients()

    @classmethod
    def default_axis(cls):
        r_cos = [5.54263, 0.184047]
        z_sin = [0.0000, 0.157481]

        # Fourier coefficients for the boundary	
        coeffs_r_cos = FourierCoefficients(coefficients=r_cos,
                                           poloidalModeNumbers=[0],
                                           toroidalModeNumbers=[0, 1],
                                           numRadialPoints=1)
        coeffs_z_sin = FourierCoefficients(coefficients=z_sin,
                                           poloidalModeNumbers=[0],
                                           toroidalModeNumbers=[0, 1],
                                           numRadialPoints=1)
        
        return cls(RCos=coeffs_r_cos, ZSin=coeffs_z_sin)

    @classmethod
    def default_boundary(cls):
        # m      0    0   0       1      1    1  
        # n      -1   0   1      -1      0    1
        r_cos = [0.0, 5.5, 0.151, 0.039, 0.26,-0.085]
        z_sin = [0.0, 0.0,-0.154, 0.040, 0.45, 0.180]

        # Fourier coefficients for the boundary	
        coeffs_r_cos = FourierCoefficients(coefficients=r_cos,
                                           poloidalModeNumbers=[0, 1],
                                           toroidalModeNumbers=[-1, 0, 1],
                                           numRadialPoints=1)
        coeffs_z_sin = FourierCoefficients(coefficients=z_sin,
                                           poloidalModeNumbers=[0, 1],
                                           toroidalModeNumbers=[-1, 0, 1],
                                           numRadialPoints=1)
        
        return cls(RCos=coeffs_r_cos, ZSin=coeffs_z_sin)

    def __call__(self, phi, theta):
        partsR = []
        partsZ = []

        i = 0
        for m in self.RCos.poloidalModeNumbers:
            for n in self.RCos.toroidalModeNumbers:
                part = self.RCos.coefficients[i] * np.cos(m * theta -
                                                          5 * n * phi)
                partsR.append(part)
                i += 1

        j = 0
        for m in self.ZSin.poloidalModeNumbers:
            for n in self.ZSin.toroidalModeNumbers:
                part = self.ZSin.coefficients[j] * np.sin(m * theta -
                                                          5 * n * phi)
                partsZ.append(part)
                j += 1
        return sum(partsR), sum(partsZ)


def startVmecString(input_data, **kwargs):
    """
    Args:
        input_data (str): filePath to input file or content of input file
    Examples:
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_input.txt')
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_boundarySymmetryTerms_input.txt')
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_boundarySymmetryTerms0_input.txt')
        # >>> startVmecString('w7x_ref_60', vmec_id='dboe_w7x_ref_60_fromOnlineString')
    """
    default_vmec_id = None
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    inFilePath = tfields.lib.in_out.resolve(input_data)
    if os.path.isfile(inFilePath):
        # input file given
        default_vmec_id = os.path.basename(inFilePath).rstrip('_input.txt')
        default_vmec_id = 'w7x_vmec_' + default_vmec_id
        with file(inFilePath, 'r') as f:
            input_data = f.read()
    if '\n' not in input_data:
        # get input file from vmec_id to restart a run
        default_vmec_id = input_data
        default_vmec_id = 'w7x_vmec_' + default_vmec_id
        run = Run(input_data)
        input_data = run.getInputString()

    vmec_id = kwargs.pop('vmec_id', default_vmec_id)
    vmec_server.service.execVmecString(input_data, vmec_id)


def vmec_id_exists(vmec_id):
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    return vmec_server.service.vmecIdentifierExists(vmec_id)


def volume_lcfs(vmec_id):
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    return vmec_server.service.getVolumeLCFS(vmec_id)


def was_successful(vmec_id):
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    try:
        success = vmec_server.service.wasSuccessful(vmec_id)
    except Exception as err:
        log = logging.getLogger()
        success = False
        log.error("@vmec_id '{vmec_id}': {err}".format(**locals()))
    return success


def existing_vmec_ids():
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    res = vmec_server.service.listIdentifiers()
    return res.ReferenceShortIds + res.VmecIds


def getBAxis(vmec_id, phi=0.):
    """
    Args:
        vmec_id (str): vmec identifier
        phi (float): phi in radian
    Returns:
        float: Bax(phi) - magnetic field magnitude on the magnetic
            axis at phi = <phi>
    """
    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    points = Points3D(vmec_server.service.getMagneticAxis(vmec_id, phi))
    res = vmec_server.service.magneticField(vmec_id, points.as_input())
    B = Points3D(res)
    return np.linalg.norm(B)


def vmec_input(**kwargs):
    """
    Args:
        **kwargs
            Necessary:
                magnetic_config (MagneticConfig)
                pressure_profile (Profile)
                current_profile (Profile)
                magneticAxis (FourierCoefficients)
                boundary (FourierCoefficients)
            Obligatory:
                maxIterationsPerSequence (int): -> NITER
                maxToroidalMagneticFlux (float): -> PHIEDGE

    """
    magnetic_config = kwargs.pop('magnetic_config')
    pressure_profile = kwargs.pop('pressure_profile')
    current_profile = kwargs.pop('current_profile')
    magneticAxis = kwargs.pop('magneticAxis')
    boundary = kwargs.pop('boundary')
    iotaProfile = kwargs.pop('iotaProfile', None)
    totalToroidalCurrent = kwargs.pop('totalToroidalCurrent',
                                      w7x.Defaults.VMEC.totalToroidalCurrent)
    maxIterationsPerSequence = kwargs.pop('maxIterationsPerSequence',
                                          w7x.Defaults.VMEC.maxIterationsPerSequence)
    maxToroidalMagneticFlux = kwargs.pop('maxToroidalMagneticFlux',
                                         w7x.Defaults.VMEC.maxToroidalMagneticFlux)
    timeStep = kwargs.pop('timeStep', w7x.Defaults.VMEC.timeStep)
    numGridPointsRadial = kwargs.pop('numGridPointsRadial',
                                     w7x.Defaults.VMEC.numGridPointsRadial)
    forceToleranceLevels = kwargs.pop('forceToleranceLevels',
                                      w7x.Defaults.VMEC.forceToleranceLevels)

    vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
    input_data = vmec_server.types.VmecInput(True)

    input_data.mgridFile = "mgrid_w7x_nv36_hires.nc"  # 'mgrid_w7x_nv36.nc'
    input_data.coilCurrents = magnetic_config.coil_currents('A')

    input_data.pressureProfile = pressure_profile.as_input()
    input_data.toroidalCurrentProfile = current_profile.as_input()
    if iotaProfile:
        input_data.iotaProfile = iotaProfile.as_input()

    input_data.freeBoundary = True
    input_data.intervalFullVacuumCalculation = 6
    input_data.numFieldPeriods = 5
    input_data.numModesPoloidal = 12
    input_data.numModesToroidal = 12
    input_data.numGridPointsPoloidal = 32
    input_data.numGridPointsToroidal = 36
    input_data.numGridPointsRadial = numGridPointsRadial
    input_data.forceToleranceLevels = forceToleranceLevels
    input_data.totalToroidalCurrent = totalToroidalCurrent
    input_data.timeStep = timeStep
    input_data.tcon0 = 2.
    input_data.maxIterationsPerSequence = maxIterationsPerSequence
    input_data.intervalConvergenceOutput = 100
    input_data.maxToroidalMagneticFlux = maxToroidalMagneticFlux
    input_data.gamma = 0

    input_data.magneticAxis = magneticAxis.as_input()
    input_data.boundary = boundary.as_input()
    return input_data


def find_run(currents_rw,
             rel_pressure_profile=[1, -1],
             rel_current_profile=[],
             delta=1e-2,
             min_beta=None,
             max_beta=None,
             min_b_axis=None,
             max_b_axis=None,
             minP0=None,
             maxP0=None,
             idContains=None,
             ready=False):
    log = logging.getLogger()
    vmec_ids = existing_vmec_ids()
    pressure_profile = (PowerSeries(coefficients=rel_pressure_profile)
                        if rel_pressure_profile is not None else None)
    current_profile = (PowerSeries(coefficients=rel_current_profile)
                      if rel_current_profile is not None else None)
    for vmec_id in vmec_ids:
        log.debug("vmec_id {vmec_id}:".format(**locals()))
        if idContains is not None:
            if not all([word in vmec_id for word in idContains]):
                log.debug("\t\t\t...vmec_id does not contain one of "
                          "idContains({idContains})".format(**locals()))
                continue

        run = Run(vmec_id)
        '''coilCurrents'''
        try:
            run_currents = run.magnetic_config.coil_currents('rw')
        except:
            log.debug("\t\t\t...error when getting magneitcConfig")
            continue
        if not run.was_successful():
            if ready:
                log.debug("\t\t\t...not successful")
                continue
            elif run.is_ready():
                log.debug("\t\t\t...not successful")
                continue
        dev = np.sqrt(sum(map(lambda x: abs((x[0] - x[1])**2),
                              zip(run_currents, currents))))

        if dev > delta:
            log.debug("\t\t\t...differing in magnetic_config by {dev}"
                      .format(**locals()))
            continue

        '''Pressure'''
        if pressure_profile is not None:
            if not isinstance(run.pressure_profile, PowerSeries):
                log.debug("\t\t\t...PressureProfile is not PowerSeries")
                continue
            p0 = run.pressure_profile.norm
            if minP0 is not None:
                if p0 < minP0:
                    log.debug("\t\t\t...p0({p0}) < minP0({minP0})"
                              .format(**locals()))
                    continue
            if maxP0 is not None:
                if p0 > maxP0:
                    log.debug("\t\t\t...p0({p0}) > maxP0({maxP0})"
                              .format(**locals()))
                    continue
            devPP = pressure_profile.deviation(run.pressure_profile)
            if devPP > delta:
                log.debug("\t\t\t...differing in relative pressure_profile by"
                          " {devPP}"
                          .format(**locals()))
                continue

        '''Current'''
        if current_profile is not None:
            if not isinstance(run.current_profile, PowerSeries):
                log.debug("\t\t\t...CurrentProfile is not PowerSeries")
                continue
            devCP = current_profile.deviation(run.current_profile)
            if devCP > delta:
                log.debug("\t\t\t...differing in relative current_profile by"
                          " {devCP}"
                          .format(**locals()))
                continue

        '''Beta'''
        if min_beta is not None or max_beta is not None:
            beta = run.beta()
        if min_beta is not None:
            if not min_beta < beta:
                log.debug("\t\t\t...min_beta({min_beta}) > beta({beta})"
                          .format(**locals()))
                continue
        if max_beta is not None:
            if not beta < max_beta:
                log.debug("\t\t\t...max_beta({max_beta}) < beta({beta})"
                          .format(**locals()))
                continue

        '''BAxis'''
        if min_b_axis is not None or max_b_axis is not None:
            b_axis = run.getBAxis()
        if min_b_axis is not None:
            if not min_b_axis < b_axis:
                log.debug("\t\t\t...min_b_axis({min_b_axis}) > b_axis({b_axis})"
                          .format(**locals()))
                continue
        if max_b_axis is not None:
            if not b_axis < max_beta:
                log.debug("\t\t\t...max_b_axis({max_b_axis}) < b_axis({b_axis})"
                          .format(**locals()))
                continue
    
        return run


class Run(object):
    RUNARGS = [
        'magnetic_config',
        'pressure_profile',
        'current_profile',
        'magneticAxis',
        'boundary']

    def __init__(self, *args, **run_kwargs):
        """
        Examples:
            >>> import w7x

            Picking up an old run
            >>> run = w7x.vmec.Run("w7x_ref_9")
            >>> run.vmec_id
            'w7x_ref_9'

            or 
            >>> run = w7x.vmec.Run(run)

            A run has the attributes:
            >>> run.vmec_id
            'w7x_ref_9'

            auto vmec_id generation
            >>> vmec_id = w7x.vmec.Run(magnetic_config=w7x.flt.MagneticConfig.default(),
            ...                        pressure_profile=w7x.vmec.PowerSeries(),
            ...                        current_profile=w7x.vmec.PowerSeries()).vmec_id
            >>> vmec_id.startswith('w7x')
            True

            magnetic_config
            >>> run.magnetic_config.coil_currents('A')
            [15000.0, 15000.0, 15000.0, 15000.0, 15000.0, 0.0, 0.0, 0.0, 0.0]

            plasma beta
            >>> run.beta()
            0.01984

        """
        self._iteration = run_kwargs.pop('iteration', 0)
        self.parent = run_kwargs.pop('parent', None)
        self._run_kwargs = {}
        self.run_kwargs = run_kwargs
        self._vmec_id = None
        if len(args) == 0:
            vmec_id = self.build_vmec_id()
        elif len(args) == 1:
            vmec_id = args[0]
        else:
            raise ValueError("Too many arguments.")
        self.vmec_id = vmec_id
        self._parsed = []

    @classmethod        
    def vacuum(cls, magnetic_config=None, **kwargs):
        if magnetic_config is None:
            raise ValueError("magnetic_config missing")
        kwargs['magnetic_config'] = magnetic_config
        kwargs['pressure_profile'] = PowerSeries()
        kwargs['current_profile'] = PowerSeries()
        if 'parent' not in kwargs:
            kwargs['magneticAxis'] = SurfaceCoefficients.default_axis()
            kwargs['boundary'] = SurfaceCoefficients.default_boundary()
            
        return cls(**kwargs)

    def __str__(self):
        string = (
            "{self.__class__} instance\n"
            "\n"
            "\t\t\tvmec_id: {self.vmec_id}\n"
            "\n"
            .format(**locals()))

        ''' add the status '''
        if not vmec_id_exists(self.vmec_id):
            status = "initializing"
        elif self.was_successful():
            status = "successful"
        else:
            status = "not successful"
        string += (
            "Status: {status}\n"
            .format(**locals()))

        ''' add the input parameters '''
        if self.parent is None:
            partent_vmec_id = "None"
        elif not vmec_id_exists(self.parent.vmec_id):
            partent_vmec_id = "unknown"
        else:
            partent_vmec_id = self.parent.vmec_id
        string += (
            "Parameters:\n"
            "\tparent: {partent_vmec_id}\n"
            "\tcoil currents (winding currents in A): {coilCurrents}\n"
            .format(
                coilCurrents=self.magnetic_config.coil_currents('A'),
                **locals()))
        string += (
            "\tpressure_profile:\n"
            "\t\tType: {self.pressure_profile.ProfileType}\n"
            "\t\tcoefficients: {self.pressure_profile.coefficients}\n"
            .format(**locals()))
        string += (
            "\tcurrentProfile:\n"
            "\t\tType: {self.current_profile.ProfileType}\n"
            "\t\tcoefficients: {self.current_profile.coefficients}\n"
            .format(**locals()))
        restKwargs = copy.deepcopy(self.run_kwargs)
        for key in restKwargs:
            if key not in self.RUNARGS:
                string += (
                    "{key}: {value}\n"
                    .format(key=key,
                            value=restKwargs[key]))

        ''' add the major results '''
        if self.was_successful():
            string += (
                "\n"
                "Results:\n"
                "\tB_Axis(phi=0): {b_axis}\n"
                "\tbeta: {beta}\n"
                "\tvolume LCFS (m^3): {volume}\n"
                "\tforce: {force}\n"
                .format(
                    b_axis=self.getBAxis(),
                    beta=self.beta(),
                    volume=self.volume_lcfs(),
                    force=self.force(),
                    **locals()))
        return string

    @property
    def vmec_id(self):
        return self._vmec_id

    @vmec_id.setter
    def vmec_id(self, vmec_id):
        if isinstance(vmec_id, Run):
            vmec_id = vmec_id.vmec_id
        self._vmec_id = vmec_id

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, str):
            parent = Run(parent)
        self._parent = parent

    @property
    def run_kwargs(self):
        """
        (dict): kwargs to pass to the vmec service
        """
        return self._run_kwargs

    @run_kwargs.setter
    def run_kwargs(self, run_kwargs):
        self._run_kwargs = run_kwargs

    @property
    def magnetic_config(self):
        """
        (w7x.flt.MagneticConfig)
        """
        magnetic_config = self.run_kwargs.get('magnetic_config', None)
        if magnetic_config is not None:
            return magnetic_config
        if self.parent is not None:
            return self.parent.magnetic_config
        if self.exists():
            vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
            currents = np.array(vmec_server.service.getCoilCurrents(self.vmec_id))
            magnetic_config = w7x.MagneticConfig.from_currents(*currents,
                                                               unit='A')
            return magnetic_config
        raise ValueError("No magnetic_config found.")

    @magnetic_config.setter
    def magnetic_config(self, config):
        self.run_kwargs['magnetic_config'] = config

    @property
    def pressure_profile(self):
        pressure_profile = self.run_kwargs.get('pressure_profile', None)
        if pressure_profile is not None:
            return pressure_profile
        if self.parent is not None:
            return self.parent.pressure_profile
        if self.exists():
            self._parse_input()
            pressure_profile = create_profile(
                ProfileType=self._input['pressureProfileProfileType'],
                coefficients=self._input['pressureProfileCoefficients'])
            return pressure_profile
        raise ValueError("No pressure_profile found.")

    @pressure_profile.setter
    def pressure_profile(self, profile):
        if profile.norm == 0:
            profile = PowerSeries(coefficients=[1e-6, -1e-6])  # very slight gradient
        self.run_kwargs['pressure_profile'] = profile

    @property
    def current_profile(self):
        current_profile = self.run_kwargs.get('current_profile', None)
        if current_profile is not None:
            return current_profile
        if self.parent is not None:
            return self.parent.current_profile
        if self.exists():
            self._parse_input()
            current_profile = create_profile(
                ProfileType=self._input['currentProfileProfileType'],
                coefficients=self._input['currentProfileCoefficients'])
            return current_profile
        raise ValueError("No current_profile found.")

    @current_profile.setter
    def current_profile(self, profile):
        self.run_kwargs['current_profile'] = profile

    @property
    def magneticAxis(self):
        magneticAxis = self.run_kwargs.get('magneticAxis', None)
        if magneticAxis is not None:
            return magneticAxis
        if self.parent is not None:
            return self.parent.magneticAxis
        if self.exists():
            self._parse_threed1()
            rcos = FourierCoefficients(coefficients=self._threed1['rac'][:2],
                                       poloidalModeNumbers=[0],
                                       toroidalModeNumbers=[0, 1],
                                       numRadialPoints=1)
            zsin = FourierCoefficients(coefficients=self._threed1['zas'][:2],
                                       poloidalModeNumbers=[0],
                                       toroidalModeNumbers=[0, 1],
                                       numRadialPoints=1)
            magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    @magneticAxis.setter
    def magneticAxis(self, surfaceCoefficients):
        self.run_kwargs['magneticAxis'] = surfaceCoefficients

    @property
    def boundary(self):
        """
        (SurfaceCoefficients): fourrier description of the vmec boundary
        """
        boundary = self.run_kwargs.get('boundary', None)
        if boundary is not None:
            return boundary
        if self.parent is not None:
            return self.parent.boundary
        if self.exists():
            # parse boundary of completed run
            self._parse_threed1()
            coeffDict = {(m, n): (rbc, zbs)
                         for m, n, rbc, zbs in zip(self._threed1['mb'],
                                                   self._threed1['nb'],
                                                   self._threed1['rbc'],
                                                   self._threed1['zbs'])}

            toroidalModeNumbers = sorted(set([x for x in self._threed1['nb']
                                              if abs(x) <= 6]))
            poloidalModeNumbers = sorted(set([x for x in self._threed1['mb']
                                              if abs(x) <= 6]))
            rbcChoice = []
            zbsChoice = []
            for m in poloidalModeNumbers:
                for n in toroidalModeNumbers:
                    if m == 0 and n < 0:
                        rbcChoice.append(0.)
                        zbsChoice.append(0.)
                        """
                        the latter would be the mathematically correct version
                        Somehow the vmec service does not handle m=0,n<0 correct
                        """
                        # rbcChoice.append(coeffDict[(m, abs(n))][0])
                        # zbsChoice.append(-coeffDict[(m, abs(n))][1])
                    else:
                        rbcChoice.append(coeffDict[(m, n)][0])
                        zbsChoice.append(coeffDict[(m, n)][1])

            rcos = FourierCoefficients(coefficients=rbcChoice,
                                       poloidalModeNumbers=poloidalModeNumbers,
                                       toroidalModeNumbers=toroidalModeNumbers,
                                       numRadialPoints=1)
            zsin = FourierCoefficients(coefficients=zbsChoice,
                                       poloidalModeNumbers=poloidalModeNumbers,
                                       toroidalModeNumbers=toroidalModeNumbers,
                                       numRadialPoints=1)
            boundary = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        elif boundary is None:
            boundary = SurfaceCoefficients.default_boundary()
        return boundary

    @boundary.setter
    def boundary(self, surfaceCoefficients):
        self.run_kwargs['boundary'] = surfaceCoefficients

    def mutate(self, **mutationKwargs):
        """
        Change the actual run settings
        """
        if 'vmec_id' in mutationKwargs:
            inst = self.__class__(mutationKwargs.pop('vmec_id'), parent=self)
        else:
            inst = self.__class__(parent=self)
        inst.run_kwargs.pop('boundary', None)
        inst.run_kwargs.pop('magneticAxis', None)
        inst.run_kwargs.update(mutationKwargs)
        return inst

    def build_vmec_id(self):
        w7x_version = w7x.__version__
        geiger_string = self.magnetic_config.geiger_string()
        pressure_norm = int(round(self.pressure_profile.norm / 1e4, 0))
        iteration = self._iteration
        vmec_id = (
            "w7x"
            "_v_{w7x_version}"
            "_id_{geiger_string}"
            "_pres_{pressure_norm:0>2d}"
            "_it_{iteration}").format(
            **locals()
        )
        if vmec_id_exists(vmec_id):
            self._iteration += 1
            return self.build_vmec_id()
        return vmec_id

    def field_period(self):
        vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
        return vmec_server.service.getFieldPeriod(self.vmec_id)

    def closest_vmec_run(self):
        vmec_ids = existing_vmec_ids()

        """
        First deviation test in relative currents
        """
        relCurrs = self.magnetic_config.coil_currents('rw')
        deviations = []
        for vmec_id in vmec_ids:
            run = Run(vmec_id)
            try:
                relCurrsRun = run.magnetic_config.coil_currents('rw')
            except:
                deviations.append(np.inf)
                continue
            if run.was_successful():
                dev = np.sqrt(sum(map(lambda x: abs((x[0] - x[1])**2),
                                      zip(relCurrsRun, relCurrs))))
            else:
                dev = np.inf
            deviations.append(dev)
        dMin = min(deviations)

        """
        Find all runs with deviation dMin
        """
        close_runs = []
        for vmec_id, dev in zip(vmec_ids, deviations):
            if dev == dMin:
                rTmp = Run(vmec_id)
                close_runs.append(rTmp)

        if len(close_runs) == 1:
            return close_runs[0]
        elif len(close_runs) == 0:
            raise ValueError("No close runs found")

        """
        Second test on deviation in pressure_profile
        """
        # p_deviations = [abs(r.pressure_profile.norm - self.norm) for r in # close_runs]
        # closest = close_runs[p_deviations.index(min(p_deviations))]
        p_deviations = []
        log = logging.getLogger()
        for r in close_runs:
            try:
                r.pressure_profile
            except Exception as err:
                log.error(str(err))
                log.warning("Probably false profile Type for vmec_id "
                            "{vmec_id}".format(vmec_id=r.vmec_id))
                continue
            p_deviations.append(self.pressure_profile.deviation(r.pressure_profile))
        closest = close_runs[p_deviations.index(min(p_deviations))]  # TODO: args is an empty sequence
        return closest

    def _complete_run_kwargs(self):
        """
        Complete the necessary arguments for starting a vmec run.
        The rest is set as default
        """
        for arg in self.RUNARGS:
            if self.run_kwargs.get(arg, None) is None:
                if self.parent is None:
                    parent = self.closest_vmec_run()
                    log = logging.getLogger()
                    log.info("Parent '{parent.vmec_id}' is "
                             "adopting me ('{self.vmec_id}')".format(**locals()))
                    self.parent = parent
                self.run_kwargs[arg] = getattr(self.parent, arg)

    def start(self):
        log = logging.getLogger()
        log.info("Preparing run {0} for start.".format(self.vmec_id))
        self._complete_run_kwargs()
        input_data = vmec_input(**self.run_kwargs)
        vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
        log.info("Starting new VMEC run ({0}).".format(self.vmec_id))
        log.info(str(self))
        vmec_server.service.execVmec(input_data, self.vmec_id)

    def shift_axis(self, shift=-0.01):
        """
        Translate the magneticAxis radially by <shift>
        """
        log = logging.getLogger()
        self.magneticAxis.RCos.coefficients[0] += shift
        log.info("Shifted axis by {shift}.".format(**locals()))

    def converge(self, iteration=0, reducedTolerance=False):
        """
        Returns:
            Run instance of converged run
        """
        log = logging.getLogger()
        if not self.exists():
            self.start()
        else:
            log.info("VMEC run ({0}) already done.".format(self.vmec_id))
        self.wait()
        if not self.was_successful():
            vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
            threed1Content = vmec_server.service.getVmecRunData(self.vmec_id, 'threed1')
            log.info("VMEC run (self.vmec_id) was not successful. - iteration"
                     ": {iteration}".format(**locals()))
            run_kwargs = copy.deepcopy(self.run_kwargs)
            changed = False
            if 'Plasma Boundary exceeded Vacuum Grid Size' in threed1Content:
                max_toroidal_magnetic_flux = run_kwargs.get('maxToroidalMagneticFlux',
                                                            w7x.Defaults.VMEC.maxToroidalMagneticFlux) * 2. / 3
                run_kwargs['maxToroidalMagneticFlux'] = max_toroidal_magnetic_flux
                log.info("Plasma Boundary exceeded Vacuum Grid Size. "
                         "New phiEdge: {max_toroidal_magnetic_flux}"
                         .format(**locals()))
                changed = True
            if iteration < 2 and 'Try increasing NITER' in threed1Content:
                run_kwargs['maxIterationsPerSequence'] = \
                    run_kwargs.get('maxIterationsPerSequence',
                                  w7x.Defaults.VMEC.maxIterationsPerSequence) + 50000
                log.info("Try increasing NITER. "
                         "New niter: {maxIterationsPerSequence}"
                         .format(maxIterationsPerSequence=run_kwargs['maxIterationsPerSequence']))
                changed = True
            if iteration == 2 and reducedTolerance:
                raise ValueError("Even the tolerance reduced run did not converge.")
            if iteration >= 2:
                log.info("Still not converged try shrinking the magneticAxis.")
                roughRunKwargs = copy.deepcopy(run_kwargs)
                forceToleranceLevels = roughRunKwargs.pop('forceToleranceLevels',
                                                          w7x.Defaults.VMEC.forceToleranceLevels)
                lastTolerance = forceToleranceLevels[-1] / 1e2
                if len(forceToleranceLevels) > 1 and lastTolerance < forceToleranceLevels[-2]:
                    lastTolerance = forceToleranceLevels[-2]
                forceToleranceLevels[-1] = lastTolerance
                roughRunKwargs['forceToleranceLevels'] = forceToleranceLevels
                log.info("Try with lower tolerance {lastTolerance}"
                         .format(**locals()))
                roughRun = self.__class__(**roughRunKwargs)
                if self.parent.was_successful():
                    roughRun.parent = self.parent
                roughRun.converge(reducedTolerance=True)
                log.info("Lower tolerance run converged.")
                magneticAxis = roughRun.run_kwargs.get('magneticAxis')
                magneticAxis.RCos.coefficients[0] -= 0.01
                run_kwargs['magneticAxis'] = magneticAxis
                log.info("Set the magneticAxis 1cm inward.")
                changed = True

            if not changed:
                log.error("No response to non converging run.")
                return self
            newRun = self.__class__(**run_kwargs)
            return newRun.converge(iteration=iteration + 1)
        log.info("Run converged successfully")
        return self

    def exists(self):
        if self.vmec_id is None:
            return False
        return vmec_id_exists(self.vmec_id)

    def is_ready(self):
        vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
        return vmec_server.service.isReady(self.vmec_id)

    def was_successful(self):
        return was_successful(self.vmec_id)

    def wait(self, sleepTime=60):
        while not self.is_ready():
            log = logging.getLogger()
            log.debug("Waiting for VMEC run "
                      "{self.vmec_id}.".format(**locals()))
            time.sleep(sleepTime)

    def getBAxis(self):
        return getBAxis(self.vmec_id)

    def volume_lcfs(self):
        self._parse_threed1()
        return self._threed1['PlasmaVolume']

    def getConfigAndPressureProfileEstimate(self, b_axis=2.5, tolerance=0.001):
        """
        Args:
            b_axis (float): magneticField strength on axis [T]
        """
        b_axisOld = self.getBAxis()
        f = b_axis / b_axisOld
        if abs(1 - f) < tolerance:
            log = logging.getLogger()
            log.warning("Tolerance of {tolerance} was met "
                        "already.".format(**locals()))
        magnetic_config = self.magnetic_config.copy()
        pressure_profile = self.pressure_profile.copy()
        magnetic_config.scale_currents(f)
        pressure_profile.scale(f ** 2)
        return magnetic_config, pressure_profile

    def _parse_input(self):
        cached = True
        if 'input' in self._parsed:
            return
        path = tfields.lib.in_out.resolve("~/tmp/VMEC/{self.vmec_id}.input.json"
                                              .format(**locals()))
        if os.path.exists(path) and cached:
            with open(path) as f:
                self._input = json.load(f)
        else:
            vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
            content = vmec_server.service.getVmecRunData(self.vmec_id, 'input')
            iterable = content.split('\n')
            content = input_transcoding.read(iterable)
            if cached:
                with open(path, 'w') as f:
                    json.dump(content, f)
            self._input = content
        self._parsed.append('input')

    def _parse_threed1(self):
        if not self.is_ready():
            raise ValueError("Calculation with vmec_id {self.vmec_id} has not finishe yet."
                             .format(**locals()))
        cached = True
        if 'threed1' in self._parsed:
            return
        filePath = tfields.lib.in_out.resolve("~/tmp/VMEC/{self.vmec_id}.threed1.json"
                                              .format(**locals()))
        if os.path.exists(filePath) and cached:
            with open(filePath) as f:
                self._threed1 = json.load(f)
        else:
            vmec_server = w7x.get_server(w7x.Server.addr_vmec_server)
            content = vmec_server.service.getVmecRunData(self.vmec_id, 'threed1')
            iterable = content.split('\n')
            content = threed1_transcoding.read(iterable)
            if cached:
                with open(filePath, 'w') as f:
                    json.dump(content, f)
            self._threed1 = content
        self._parsed.append('threed1')

    def getInputMagneticAxis(self):
        self._parse_input()
        rac, zas = zip(self._input['value0'], self._input['value1'])
        rcos = FourierCoefficients(coefficients=list(rac),
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=list(zas),
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    def getMagneticAxis(self):
        self._parse_threed1()
        rcos = FourierCoefficients(coefficients=self._threed1['rac'][:2],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=self._threed1['zas'][:2],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    def getInputBoundary(self):
        self._parse_input()
        coeffDict = {(m, n): (rbc, zbs)
                     for m, n, rbc, zbs in zip(self._input['m'],
                                               self._input['n'],
                                               self._input['rbc'],
                                               self._input['zbs'])}

        toroidalModeNumbers = sorted(set([x for x in self._input['n']
                                          if abs(x) <= 6]))
        poloidalModeNumbers = sorted(set([x for x in self._input['m']
                                          if abs(x) <= 6]))
        rbcChoice = []
        zbsChoice = []
        for m in poloidalModeNumbers:
            for n in toroidalModeNumbers:
                if m == 0 and n < 0:
                    rbcChoice.append(coeffDict[(m, abs(n))][0])
                    zbsChoice.append(-coeffDict[(m, abs(n))][1])
                else:
                    rbcChoice.append(coeffDict[(m, n)][0])
                    zbsChoice.append(coeffDict[(m, n)][1])

        rcos = FourierCoefficients(coefficients=rbcChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=zbsChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        boundary = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return boundary

    def beta(self):
        self._parse_threed1()
        return self._threed1['forceIter'][-1]['BETA'][-1]

    def i_tor(self):
        self._parse_input()
        return self._input['i_tor']

    def force(self):
        self._parse_threed1()
        forceIter = self._threed1['forceIter'][-1]
        attrs = ['FSQR', 'FSQZ', 'FSQL']
        return max([forceIter[attr][-1] for attr in attrs])

    def phi_edge_estimate(self, min_volume=25, max_volume=30, island_width=0.075):
        """
        Args:
            min_volume(float): minimal volume in m^3
            max_volume(float): maximal volume in m^3
            island_width(float): radial width of the major islands in m.
                needed to find the maximal radius in order to
                find flux surfaces that are not bound by major islands
        """
        self._parse_threed1()
        p0, p1, p2, p3, p4 = parameters('p0, p1, p2, p3, p4')

        """
        Fit iota(r) with known plasma volume -> V = 2 pi^2 R r^2
        """
        R = self._threed1['MajorRadius']
        rmaxCalc = np.sqrt(self.volume_lcfs() / (2 * np.pi**2 * R))
        rValues = np.array(self._threed1["S"]) * rmaxCalc
        iotaValues = self._threed1["IOTA"]
        fluxValues = self._threed1["TOROIDAL_FLUX"]

        iota = Variable('iota')
        r = Variable('r')
        rPoly = p0 + p1 * r + p2 * r ** 2 + p3 * r ** 3 + p4 * r ** 4
        iotaPoly = p0 + p1 * iota + p2 * iota ** 2 + p3 * iota ** 3 + p4 * iota ** 4
        iotaVsR = fit(rPoly, rValues, iotaValues)
        rVsIota = fit(iotaPoly, iotaValues, rValues)

        """
        Find max r
            -> greater than min_volume
            -> smaller than max_volume
            -> not bound by major islands
        """
        rmaxUser = np.sqrt(max_volume / (2 * np.pi**2 * R))
        rminUser = np.sqrt(min_volume / (2 * np.pi**2 * R))

        if rmaxCalc < rminUser:
            rmaxCalc = 0.6 * (rmaxUser + rminUser)
        rmax = min((rmaxCalc, rmaxUser))
        iIsland = [4. / 5., 5. / 5., 6. / 5.]
        rIsland = [rVsIota.subs(iota, i) for i in iIsland]
        for ri in rIsland:
            if abs(rmax - ri) < 0.5 * island_width:
                rmax = ri - 0.5 * island_width
                break

        """
        fit flux(iota)
        """
        toroidalFlux = p0 + p1 * iota + p2 * iota ** 2 + p3 * iota ** 3 + p4 * iota ** 4
        fluxVsIota = fit(toroidalFlux, iotaValues, fluxValues)

        iotaMax = iotaVsR.subs(r, rmax)
        return fluxVsIota.subs(iota, iotaMax)


def getP0Estimate(beta_scan_runs, beta, normTolerance=500):
    ''' Make shure, you fit on the same bField strenghts '''
    norms = [r.magnetic_config.coil_currents('Aw')[0] for r in beta_scan_runs]
    if not len(set(norms)) < 2:
        raise ValueError("Runs of beta scan have difference coilCurrent norms"
                         "({norms})".format(**locals()))

    p0s = [0] + [r.pressure_profile.norm for r in beta_scan_runs]
    betas = [0] + [r.beta() for r in beta_scan_runs]

    a, b = parameters('a, b')
    x, y = variables('x, y')
    model = Model({y: a * x + b})
    fit = Fit(model, x=p0s, y=betas)
    res = fit.execute()
    fun = model[y]
    fun = fun.subs(a, res.params['a'])
    fun = fun.subs(b, res.params['b'])
    iFun = sympy.solve(y - fun, x)[0]
    p0 = iFun.subs(y, beta)

    return p0


def adjust_beta(currents_rw, beta, b_axis=2.5, rel_pressure_profile=[1, -1],
                rel_current_profile=[0, 1, -1], totalToroidalCurrent=None,
                beta_precision=0.001, beta_scan_runs=None):
    """
    Args:
        currents_rw (parent or relativeCurrents): 7 ratios (1 winding emulation)
        beta (float): beta = 2 * mu_0 * <p> / <B^2>
        b_axis (float): B_toroidal on the axis (s=0). Usually: 2.5
        dIota (float): delta iota to one of the three edge resonances (4/5, 5/5,
            6/5
    """
    log = logging.getLogger()

    '''0) Prepare'''
    if beta_scan_runs is None:
        beta_scan_runs = []
    else:
        beta_scan_runs = [Run(r) for r in beta_scan_runs]
    if len(beta_scan_runs) > 0:
        norm = beta_scan_runs[0].magnetic_config.coil_currents('Aw')[0]
    else:
        norm = 12000 * 108

    magnetic_config = w7x.MagneticConfig.from_currents(
        *currents_rw,
        unit='rw',
        scale=norm)
    current_profile = PowerSeries(coefficients=rel_current_profile)
    currentKwargs = dict(
        current_profile=current_profile,
        totalToroidalCurrent=totalToroidalCurrent)

    betaScanRunKwargs = dict(
        magnetic_config=magnetic_config,
        maxIterationsPerSequence=60000,
        numGridPointsRadial=[4, 9, 28, 51],
        forceToleranceLevels=[1e-3, 1e-5, 1e-9, 1e-11])
    betaScanRunKwargs.update(currentKwargs)

    if len(beta_scan_runs) == 0:
        '''0) Run initial beta scan run'''
        pressure_profile = PowerSeries(
            coefficients=[6e4 * x for x in rel_pressure_profile])
        run = Run(pressure_profile=pressure_profile,
                  **betaScanRunKwargs)
        run.converge()
        if not run.was_successful():
            raise RuntimeError("First run was not successful.")
        else:
            beta_scan_runs.append(run)

    pressure_profile = PowerSeries(coefficients=rel_pressure_profile)
    '''1) Find correct p0 '''
    log.info("1) estimate p0")
    matching_beta_runs = {}
    for run in beta_scan_runs:
        # any run already has the correct beta?
        if abs(run.beta() - beta) < beta_precision:
            matching_beta_runs[run.force()] = run
    if matching_beta_runs:
        # get most precise run from the matching ones
        grand_parent = matching_beta_runs[min(matching_beta_runs.keys())]
        log.info("Found run with correct beta in given runs: "
                 "{grand_parent.vmec_id}".format(**locals()))
    else:
        # approach correct beta.
        pDev = [pressure_profile.deviation(r.pressure_profile)
                for r in beta_scan_runs]
        greatGrandParent = beta_scan_runs[pDev.index(min(pDev))]
        while True:
            p0 = getP0Estimate(beta_scan_runs, beta=beta)
            phiEdge = greatGrandParent.phi_edge_estimate()
            pressure_profile.norm = p0
            grand_parent = Run(parent=greatGrandParent,
                              pressure_profile=pressure_profile,
                              maxToroidalMagneticFlux=phiEdge,
                              **betaScanRunKwargs)
            log.info("Start run with p0 estimate: {p0}. "
                     "Also adjust phiEdge to {phiEdge}"
                     .format(**locals()))
            grand_parent.converge()
            foundBeta = grand_parent.beta()
            if abs(foundBeta - beta) < beta_precision:
                log.info("Retrieved beta({foundBeta}) matches "
                         "Requested({beta}) within tolerance.".format(**locals()))
                break
            else:
                log.info("Retrieved beta({foundBeta}) not close enough to "
                         "Requested({beta}).".format(**locals()))
                greatGrandParent = grand_parent
                beta_scan_runs.append(greatGrandParent)

    '''2) Become more precise '''
    log.info("2) calculate more precise")
    force_tolerance = 1e-12
    if grand_parent.force() < force_tolerance:
        parent = grand_parent
        log.info("Forces in grand_parent are sufficiently small. ")
    else:
        parent = grand_parent.mutate(
            maxIterationsPerSequence=60000,
            numGridPointsRadial=[4, 9, 28, 51],
            forceToleranceLevels=[1e-3, 1e-5, 1e-9, force_tolerance])
        parent.converge(iteration=2)

    '''3) Find phiEdge and magnetic_config/p0 for correct Volume/b_axis '''
    log.info("3) Get phiEdge and magnetic_config/p0 estimate for correct "
                  "Volume/b_axis")
    phiEdge = -1.8  # parent.phi_edge_estimate()
    magnetic_config, pressure_profile = parent.getConfigAndPressureProfileEstimate()

    '''4) Run again with parameters found'''
    log.info("4) converge run with phiEdge = {phiEdge} and magnetic_config"
             "to reach b_axis = {b_axis}".format(**locals()))
    final_force_tolerance = 1e-14
    final_run = Run(maxToroidalMagneticFlux=phiEdge,
                    maxIterationsPerSequence=100000,
                    magnetic_config=magnetic_config,
                    pressure_profile=pressure_profile,
                    forceToleranceLevels=[1e-3, 1e-5, 1e-9, final_force_tolerance],
                    parent=parent,
                    **currentKwargs)
    final_run.converge()
    log.info(str(final_run))
    return final_run


if __name__ == '__main__':
    import doctest
    import loggingTools
    loggingTools.setLevel(0)
    # import doctest
    # doctest.run_docstring_examples(Run.__init__, globals())

    i_tors = []
    runs = []
    # for currents_rw in [w7x.config.Defaults.MagneticConfig.standard_rw]:
    for currents_rw in [w7x.config.Defaults.MagneticConfig.high_iota_b_rw]:  # TODO
        # for currents_rw in [w7x.config.Defaults.MagneticConfig.high_iota_rw]:  # TODO
        #                     w7x.config.Defaults.MagneticConfig.inward_shifted_rw,
        #                     w7x.config.Defaults.MagneticConfig.outward_shifted_rw,
        #                     w7x.config.Defaults.MagneticConfig.low_iota_a_rw,
        #                     w7x.config.Defaults.MagneticConfig.low_iota_b_rw,
        #                     w7x.config.Defaults.MagneticConfig.high_iota_a_rw,
        #                     w7x.config.Defaults.MagneticConfig.high_iota_b_rw,]:
        magnetic_config = w7x.flt.MagneticConfig.from_currents(
            *currents_rw,
            unit='rw')
        # initial_run = Run.vacuum(
        #     magnetic_config=magnetic_config,
        #     parent='dboe_id_1000_1000_1000_1000_+0000_-0250_v_00_pres_09_it_3')
        initial_run = Run('w7x_v_0.1.0.dev8_id_1000_1000_1000_1000_+0000_-0250_pres_00_it_7')
        initial_run = initial_run.converge()

        # for i_tor in [0.]:
        for i_tor in [0. + i * 5000 for i in range(10, 100) if i * 5000 < 51000]:
            run = adjust_beta(magnetic_config.coil_currents(unit='rw'),
                              0.0, b_axis=2.5, rel_pressure_profile=[1, -1],
                              rel_current_profile=[0, 1, -1],
                              totalToroidalCurrent=float(i_tor),
                              beta_precision=0.001,
                              beta_scan_runs=[initial_run])
            runs.append(run)
            i_tors.append(i_tor)
            print(run, i_tor)
            print('_'*100)
    for run, i_tor in zip(runs, i_tors):
        print(run.vmec_id, i_tor)
    from IPython import embed; embed()
    quit()


    pressure_profile = PowerSeries(coefficients=[1e-6, -1e-6])
    pressure_profile.norm = 0
    run = Run(magnetic_config=magnetic_config,
              pressure_profile=pressure_profile,
              totalToroidalCurrent=0)
    print(run.pressure_profile.coefficients)
    quit()
    run = run.closest_vmec_run()
    print(run.vmec_id)
    print(run.beta())
    from IPython import embed; embed()

    quit()
    doctest.testmod()
