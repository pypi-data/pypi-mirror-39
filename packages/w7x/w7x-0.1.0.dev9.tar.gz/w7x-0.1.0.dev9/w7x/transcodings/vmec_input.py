"""
input.txt file transcoding for vmec output
Yet reading only
"""
import transcoding as tc
import logging


def get_transcoding():
    def f_read_number_string(number_string, name, dtype=float):
        try:
            return {name: float(number_string)}
        except:
            return None

    def f_read_equal(line, name, event=None, dtype=float):
        """
        Read lines like "abc = 42.0"
        """
        if event is not None:
            if not event(line):
                return None
        _, _, number_string = line.rpartition('=')
        return f_read_number_string(number_string, name, dtype=dtype)
        
    
    """
    Tolerance
    """
    t_tolerance = tc.Trigger(
        lambda x: 'FTOL_ARRAY' in x)
    b_tolerance = tc.List(
        tc.Pattern("{forceToleranceLevels:f}",
                   read_method=tc.read_method(f_read_number_string,
                                              'forceToleranceLevels')),
        separator=' ',
        prefix=tc.Margin.alternatives(' FTOL_ARRAY = ', 'FTOL_ARRAY = '),
        start=t_tolerance)
    
    """
    Phi edge
    """
    t_phiEdge = tc.Trigger(
        lambda x: 'PHIEDGE' in x)
    b_phiEdge = tc.Block(
        tc.Pattern(" PHIEDGE = {maxToroidalMagneticFlux:f}",
                   read_method=tc.read_method(f_read_equal,
                                              'maxToroidalMagneticFlux',
                                              lambda x: 'PHIEDGE' in x)),
        start=t_phiEdge)
    
    """
    radial resolution
    """
    t_pressureProfile = tc.Trigger(
        lambda x: "PMASS_TYPE" in x or "IPMASS" in x,
        delay=0)
    t_radial = tc.Trigger(
        lambda x: 'NS_ARRAY' in x)
    b_radial = tc.List(
        tc.Pattern("{numGridPointsRadial:d}",
                   read_method=tc.read_method(f_read_number_string,
                                              'numGridPointsRadial')),
        separator=' ',
        prefix=tc.Margin.alternatives(' NS_ARRAY = ', 'NS_ARRAY = '),
        start=t_radial,
        barrier=t_pressureProfile)
    
    """
    Pressure Profile
    """
    t_pressureProfileBarrier = tc.Trigger(
        lambda x: "AM = " in x or " AM = " in x or " AM_AUX_F = " in x,
        delay=0)
    
    def f_pressureProfileHead(line):
        if 'PMASS_TYPE' in line:
            return f_read_equal(line,
                                'pressureProfileProfileType')
        if "IPMASS" in line:
            lut = {0: 'power_series',
                   1: 'two_Lorentz',
                   11: 'Akima_spline',
                   13: 'cubic_spline'}
            ip = int(line.split('=')[1])
            return {'pressureProfileProfileType': lut[ip]}
        return None
    
    b_pressureProfileHead = tc.Block(
        tc.Pattern("PMASS_TYPE = '{pressureProfileProfileType}'",
                   read_method=tc.read_method(f_pressureProfileHead)),
        start=t_pressureProfile,
        barrier=t_pressureProfileBarrier)
    b_pressureProfile = tc.List(
        tc.Pattern("{pressureProfileCoefficients:f}",
                   read_method=tc.read_method(f_read_number_string,
                                              'pressureProfileCoefficients')),
        separator=' ',
        rigid=False,
        prefix=tc.Margin.alternatives(' AM = ', 'AM = ', 'AM_AUX_F = '))
    
    """
    Current Profile
    """
    t_currentProfile = tc.Trigger(
        lambda x: "PCURR_TYPE" in x or "IPCURR" in x,
        delay=0)
    t_currentProfileBarrier = tc.Trigger(
        lambda x: "AC = " in x or " AC = " in x or " AC_AUX_F = " in x,
        delay=0)
    t_rAxis_start = tc.Trigger(lambda x: "RAXIS" in x, delay=0)
    
    def f_currentProfileHead(line):
        if 'PCURR_TYPE' in line:
            return f_read_equal(line,
                                'currentProfileProfileType')
        if "IPCURR" in line:
            lut = {0: 'power_series',
                   1: 'sum_atan',
                   2: 'sum_atan',
                   11: 'Akima_spline_l',
                   12: 'Akima_spline_lp',
                   13: 'cubic_spline_l',
                   14: 'cubic_spline_lp'}
            ip = int(line.split('=')[1])
            return {'currentProfileProfileType': lut[ip]}
        return None
    
    b_currentProfileHead = tc.Block(
        tc.Pattern("PCURR_TYPE = '{currentProfileProfileType}'",
                   read_method=tc.read_method(f_currentProfileHead)),
        start=t_currentProfile,
        barrier=t_currentProfileBarrier,
        default={'currentProfileProfileType': 'power_series'})
    b_currentProfile = tc.List(
        tc.Pattern("{currentProfileCoefficients:f}",
                   read_method=tc.read_method(f_read_number_string,
                                              'currentProfileCoefficients')),
        separator=' ',
        prefix=tc.Margin.alternatives('AC = ', ' AC = ', 'AC_AUX_F = '),
        rigid=False,
        barrier=t_rAxis_start,
        default={'currentProfileCoefficients': []})
    
    b_rAxis = tc.List(
        "{RAXIS:g}",
        separator=' ',
        prefix=tc.Margin.alternatives("{tmp:5} = ", " {tmp:5} = "),
        rigid=False,
        start=t_rAxis_start)
    t_zAxis_start = tc.Trigger(lambda x: "ZAXIS" in x, delay=0)
    b_zAxis = b_rAxis.copy()
    b_zAxis.patterns = "{ZAXIS:g}"
    b_zAxis.start = t_zAxis_start
    t_boundary_stop = tc.Trigger(lambda x: "/" in x, delay=0)
    
    def f_boundary(line):
        if 'rbc' in line or 'RBC' in line:
            splt = line.split(',')
            if '' in splt:
                splt.remove('')
            if len(splt) != 4:
                return None
            vals = {'n': int(splt[0].split('(')[1]),
                    'm': int(splt[1].split(')')[0]),
                    'rbc': float(splt[1].split('=')[1]),
                    'nz': int(splt[2].split('(')[1]),
                    'mz': int(splt[3].split(')')[0]),
                    'zbs': float(splt[3].split('=')[1])}
            return vals
        return None
    
    b_boundary = tc.Table(
        tc.Pattern(" RBC({n:d},{m:d}) = {rbc:g}  ZBS({nz:d},{mz:d}) = {zbs:g}",
                   read_method=tc.read_method(f_boundary)),
        stop=t_boundary_stop)
    
    
    class CorrectedTranscoding(tc.Transcoding):
        def read(self, inp):
            newInp = []
            for line in inp:
                if "ZAXIS" in line:
                    if 'rbc' in line:
                        newInp.append(line.split('rbc')[0])
                        newInp.append('rbc' + line.split('rbc')[1])
                    else:
                        break
                newInp.append(line)
            else:
                inp = newInp
            d = super(CorrectedTranscoding, self).read(inp)
            if "pressureProfileProfileType" not in d:
                d["pressureProfileProfileType"] = 'power_series'
            if "currentProfileProfileType" not in d:
                d["currentProfileProfileType"] = 'power_series'
            return d
    
    
    transcoding = CorrectedTranscoding(b_tolerance,
                                       b_phiEdge,
                                       b_radial,
                                       b_pressureProfileHead,
                                       b_pressureProfile,
                                       b_currentProfileHead,
                                       b_currentProfile,
                                       b_rAxis,
                                       b_zAxis,
                                       b_boundary)
    return transcoding


if __name__ == '__main__':
    import w7x
    import loggingTools
    loggingTools.setLevel(1)
    run = w7x.vmec.Run("w7x_ref_9")
    run._parse_input()
    print(run._input)
