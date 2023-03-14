import platform as _pltfm
import ctypes
import numpy as _np
from multiprocessing import Pool, RawValue, RawArray

global NPOINTS
global NREFS
global NCOL
global C
global FNUM
global POINTS
global TREFS
global REFS
global ALPHAS
global TABLE
global NSAMP
global TSTART
global TS

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

_trig.calcindices.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int))
_trig.calcindices.restype = ctypes.POINTER(ctypes.c_int)

def __gentables__(index):
    global _trig

    # generate transmit tabs
    _ref = (NCOL*ctypes.c_float)(*[REFS[NCOL*index+ind] for ind in range(NCOL)])
    alpha = float(ALPHAS[index])
    __n = _np.zeros(NCOL, dtype=ctypes.c_float)
    __n[0] = _np.sin(alpha)
    __n[NCOL-1] = _np.cos(alpha)
    _ndir = __n.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _tautx = _trig.pwtxengine(NPOINTS, C, TREFS[index], _ref, _ndir, POINTS)

    # generate receive tabs
    _taurx = _trig.rxengine(NPOINTS, C, _ref, POINTS)

    # generate mask
    __n = _np.zeros(NCOL, dtype=ctypes.c_float)
    __n[0] = 1
    _napp = __n.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    _mask = _trig.genmask3D(NPOINTS, FNUM, ctypes.c_int(1), FNUM, ctypes.c_int(1), _napp, _ndir, _ref, POINTS)
    
    # get delay table
    inds = _trig.calcindices(NPOINTS, NSAMP, TSTART, TS, _tautx, _taurx, _mask)
    
    tau = _np.array(NPOINTS)
    for ind in range(NPOINTS):
        tau[ind] = inds[ind]
    return tau

def __init_table__():
    global TABLE
    TABLE = RawArray(ctypes.c_int, NREFS*NPOINTS)

    with Pool() as p:
        tau = p.map(__gentables__, range(NREFS))

    # print(_tables)
    
    # for ind, _table in enumerate(_tables):
    #     for indt in range(NPOINTS):
    #         TABLE[ind*NPOINTS + indt] = _table[indt]

class PWBeamformer():
    """Right now, assumes all points are within y=0"""
    def __init__(self, c, fnum, points, trefs, refs, alphas, nsamp, ts, tstart):
        global NPOINTS
        global NREFS
        global NCOL
        global C
        global FNUM
        global POINTS
        global TREFS
        global REFS
        global ALPHAS
        global NSAMP
        global TSTART
        global TS

        # initialize shared values
        NPOINTS = points.shape[0]
        NREFS = len(trefs)
        NCOL = points.shape[0]
        C = RawValue(ctypes.c_float, c)
        FNUM = RawValue(ctypes.c_float, fnum)
        NSAMP = int(nsamp)
        TSTART = RawValue(ctypes.c_float, tstart)
        TS = RawValue(ctypes.c_float, ts)

        # intialize shared points array
        POINTS = RawArray(ctypes.c_float, NPOINTS*NCOL)
        _points = _np.ascontiguousarray(points, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(NCOL*NPOINTS):
            POINTS[ind] = _points[ind]

        # initialize shared reference time array
        TREFS = RawArray(ctypes.c_float, NREFS)
        _trefs = _np.ascontiguousarray(trefs, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(NREFS):
            TREFS[ind] = _trefs[ind]

        # intialize refgerence points array
        REFS = RawArray(ctypes.c_float, NREFS*NCOL)
        _refs = _np.ascontiguousarray(refs, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(NREFS*NCOL):
            REFS[ind] = _refs[ind]

        # initialize shared alphas array
        ALPHAS = RawArray(ctypes.c_float, NREFS)
        _alphas = _np.ascontiguousarray(alphas, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(NREFS):
            ALPHAS[ind] = _alphas[ind]

        __init_table__()