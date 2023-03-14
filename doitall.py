import platform as _pltfm
import ctypes
import numpy as _np
from multiprocessing import Pool, RawValue, RawArray

# determine the OS
if _pltfm.uname()[0] == "Windows":
    name = "./_trig.dll"
elif _pltfm.uname()[0] == "Linux":
    name = "./_trig.so"
else:
    name = "./_trig.dylib"

# load the c library
_trig = ctypes.CDLL(name)

# c function definitions inputs and outputs
_trig.pwtxengine.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
_trig.pwtxengine.restype = ctypes.POINTER(ctypes.c_float)

_trig.rxengine.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
_trig.rxengine.restype = ctypes.POINTER(ctypes.c_float)

_trig.genmask3D.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
_trig.genmask3D.restype = ctypes.POINTER(ctypes.c_int)

def calc_indices(N, c, tref, ref, n, points, tstart, Ts, Ntrace, Ntau):
    """Calculate delay tabs and return corresponding indices
    
    """

def maketables(**kwargs):
    """Calculate delay from transmission to a given point

    Parameters:
    ----
    `c`: speed of sound in m/s
    `tref`: delay tab of reference in s
    'ref`: a length 3 vector corresponding to reference lcation [m, m, m]
    'n`: normal vector of wave propogation
    `points`: N by 3 array of point coordinates N*[m, m, m]
    """
    points = kwargs['points']
    c = kwargs['c']
    tref = kwargs['tref']
    ref = kwargs['ref']
    n = kwargs['n']

    N = points.shape[0]
    _N = ctypes.c_int(N)
    _c = ctypes.c_float(c)
    _tref = ctypes.c_float(tref)
    _ref = _np.ascontiguousarray(ref, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _n = _np.ascontiguousarray(n, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _points = _np.ascontiguousarray(points, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    _tautx = _trig.pwtxengine(_N, _c, _tref, _ref, _n, _points)
    
    return None

class PWBeamformer():
    """Right now, assumes all points are within y=0"""
    def __init__(self, c, trefs, refs, points, nprops, fnums):
        self.points = _np.ascontiguousarray(points, dtype=ctypes.c_float)