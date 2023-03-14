import platform as _pltfm
import ctypes
import numpy as _np
from time import time

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

def pwtxengine(c : float, tref : float, ref:_np.array, n:_np.array, points:_np.array):
    """Calculate delay from transmission to a given point

    Parameters:
    ----
    `c`: speed of sound in m/s
    `tref`: delay tab of reference in s
    'ref`: a length 3 vector corresponding to reference lcation [m, m, m]
    'n`: normal vector of wave propogation
    `points`: N by 3 array of point coordinates N*[m, m, m]
    """
    N = points.shape[0]
    _N = ctypes.c_int(N)
    _c = ctypes.c_float(c)
    _tref = ctypes.c_float(tref)
    _ref = _np.ascontiguousarray(ref).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _n = _np.ascontiguousarray(n).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _points = _np.ascontiguousarray(points).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    _tautx = _trig.pwtxengine(_N, _c, _tref, _ref, _n, _points)
    
    tautx = _np.array([float(_tautx[ind]) for ind in range(N)])
    return tautx

def rxengine(c : float, tref : float, ref:_np.array, n:_np.array, points:_np.array):
    """Calculate distance from points to ref

    Parameters:
    ----
    `c`: speed of sound in m/s
    `tref`: delay tab of reference in s
    'ref`: a length 3 vector corresponding to reference lcation [m, m, m]
    'n`: normal vector of wave propogation
    `points`: N by 3 array of point coordinates N*[m, m, m]
    """
    N = points.shape[0]
    _N = ctypes.c_int(N)
    _c = ctypes.c_float(c)
    _tref = ctypes.c_float(tref)
    _ref = _np.ascontiguousarray(ref).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _n = _np.ascontiguousarray(n).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _points = _np.ascontiguousarray(points).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    _taurx = _trig.pwtxengine(_N, _c, _tref, _ref, _n, _points)
    
    taurx = _np.array([float(_taurx[ind]) for ind in range(N)])
    return taurx

def genmask3D(fmaj:float, dynmaj:bool, fmin:float, dynmin:float, n:_np.array, focus:_np.array, ref:_np.array, points:_np.array):
    """Calculate mask"""
    N = points.shape[0]
    _N = ctypes.c_int(N)
    _fmaj = ctypes.c_float(fmaj)
    _fmin = ctypes.c_float(fmin)
    _dynmaj = ctypes.c_int(-1) if dynmaj else ctypes.c_int(0)
    _dynmin = ctypes.c_int(-1) if dynmin else ctypes.c_int(0)
    _focus = _np.ascontiguousarray(focus).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _ref = _np.ascontiguousarray(ref).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _n = _np.ascontiguousarray(n).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _points = _np.ascontiguousarray(points).astype(ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    _mask = _trig.genmask3D(_N, _fmaj, _dynmaj, _fmin, _dynmin, _n, _focus, _ref, _points)

    mask = _np.array([(not _mask[ind] == 0) for ind in range(N)])
    return mask


