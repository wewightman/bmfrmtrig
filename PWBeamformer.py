import platform as _pltfm
import ctypes
import numpy as np
from multiprocessing import Pool, RawValue, RawArray
from Beamformer import Beamformer, __BMFRM_PARAMS__

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

class PWBeamformer(Beamformer):
    """Right now, assumes all points are within y=0"""
    def __init__(self, c, fnum, points, alphas, trefs, refs, ts, tstart, nsamp:int):
        Beamformer.__init__()

        def putsingles(data, dtype):
            res = []
            for datum in data:
                res.append(RawValue(dtype, datum))
            return res

        def putarrays(data, dtype):
            res = []
            for ind in range(data.shape[0]):
                res.append(RawArray(dtype, np.ascontiguousarray(data[ind], dtype=dtype)))
            return res

        # copy singleton vectors to param structure
        params = {}
        params['npoints'] = points.shape[0]
        params['nacq'] = refs.shape[0]
        params['c'] = c
        params['fnum'] = fnum
        params['nsamp'] = nsamp
        params['ts'] = ts
        params['tstart'] = tstart

        params['trefs'] = putsingles(trefs, ctypes.c_float)
        params['alphas'] = putsingles(alphas, ctypes.c_float)

        params['refs'] = putarrays(refs, ctypes.c_float)

        # copy large arrays to ctypes
        params['points'] = RawArray(ctypes.c_float, params['npoints']*3)
        _points = np.ascontiguousarray(points, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(len(_points)):
            params['points'][ind] = _points[ind]

        # make a buffer of time index arrays
        params['tinds'] = []
        for ind in range(params['nsamp']):
            params['tinds'].append(RawArray(ctypes.c_float, params['nsamp']))
        
        # make a buffer of mask arrays
        params['masks'] = []
        for ind in range(params['nsamp']):
            params['masks'].append(RawArray(ctypes.c_uint8, params['nsamp']))
        
        __BMFRM_PARAMS__[self.id] = params

        self.__init_tabs__()
        self.__init_tabs__()

    def __init_tabs__(self):
        return super().__init_tabs__()
    
    def __init_masks__(self):
        return super().__init_masks__()