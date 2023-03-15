import ctypes
import numpy as np
import ctypes
from multiprocessing import Pool, RawValue, RawArray
from Beamformer import Beamformer, __BMFRM_PARAMS__

# python ctype wrappers for c engines
import trig

class PWBeamformer(Beamformer):
    """Right now, assumes all points are within y=0"""
    def __init__(self, c, fnum, points, alphas, trefs, refs, ts, tstart, nsamp:int):
        Beamformer.__init__(self)

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
        params['nacqs'] = refs.shape[0]
        params['c'] = c
        params['fnum'] = fnum
        params['nsamp'] = nsamp
        params['ts'] = ts
        params['tstart'] = tstart

        params['trefs'] = putsingles(trefs, ctypes.c_float)
        params['alphas'] = alphas

        params['refs'] = putarrays(refs, ctypes.c_float)

        # copy large arrays to ctypes
        params['points'] = RawArray(ctypes.c_float, params['npoints']*3)
        _points = np.ascontiguousarray(points, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(params['npoints']*3):
            params['points'][ind] = _points[ind]

        # make a buffer of time index arrays
        params['tinds'] = []
        for ind in range(params['nacqs']):
            params['tinds'].append(RawArray(ctypes.c_int, params['npoints']))
        
        # make a buffer of mask arrays
        params['masks'] = []
        for ind in range(params['nacqs']):
            params['masks'].append(RawArray(ctypes.c_int, params['npoints']))

        __BMFRM_PARAMS__[self.id] = params

        self.__init_masks__()
        self.__init_tabs__()
    
    def __gen_tab__(self, ind):
        # load parameters
        params = __BMFRM_PARAMS__[self.id]
        npoints = ctypes.c_int(params['npoints'])
        nsamp = ctypes.c_int(params['nsamp'])
        ref = params['refs'][ind]
        tref = params['trefs'][ind]
        c = ctypes.c_float(params['c'])
        tstart = ctypes.c_float(params['tstart'])
        ts = ctypes.c_float(params['ts'])
        mask = params['masks'][ind]
        tind = params['tinds'][ind]
        alpha = float(params['alphas'][ind])
        norm = np.ascontiguousarray([np.sin(alpha), 0, np.cos(alpha)], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        # calculate time delays
        tautx = trig.pwtxengine(npoints, c, tref, ref, norm, params['points'])
        taurx = trig.rxengine(npoints, c, ref, params['points'])
        tau = trig.sumvecs(npoints, tautx, taurx, 0)
        trig.freeme(tautx)
        trig.freeme(taurx)

        # calculate index to select
        trig.calcindices(npoints, nsamp, tstart, ts, tau, mask, tind)
        trig.freeme(tau)
        pass

    def __gen_mask__(self, ind):
        # load parameters
        params = __BMFRM_PARAMS__[self.id]
        npoints = ctypes.c_int(params['npoints'])
        ref = params['refs'][ind]
        fnum = ctypes.c_float(params['fnum'])
        alpha = float(params['alphas'][ind])
        mask = params['masks'][ind]
        focus = np.ascontiguousarray([np.sin(alpha), 0, np.cos(alpha)], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        norm = np.ascontiguousarray([1, 0, 0], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        # generate mask
        trig.genmask3D(npoints, fnum, ctypes.c_int(1), fnum, ctypes.c_int(1), norm, focus, ref, params['points'], mask)

    def __init_tabs__(self):
        with Pool() as p:
            p.map(self.__gen_tab__, range(__BMFRM_PARAMS__[self.id]['nacqs']))
    
    def __init_masks__(self):
        with Pool() as p:
            p.map(self.__gen_mask__, range(__BMFRM_PARAMS__[self.id]['nacqs']))