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
        print("Initializing a PWBeamformer...")
        Beamformer.__init__(self)

        def putsingles(data, dtype):
            res = []
            for datum in data:
                res.append(RawValue(dtype, datum))
            return res

        def putarrays(data, dtype):
            res = []
            for ind in range(data.shape[0]):
                res.append(RawArray(dtype, data.shape[1]))
                for indd in range(data.shape[1]):
                    res[ind][indd] = dtype(data[ind,indd])
            return res
        
        print("  Formatting input parameters...")
        # copy singleton vectors to param structure
        params = {}
        params['npoints'] = points.shape[0]
        params['nacqs'] = refs.shape[0]
        params['c'] = c
        params['fnum'] = fnum
        params['nsamp'] = nsamp
        params['ts'] = ts
        params['tstart'] = tstart
        params['alphas'] = alphas
        params['refs'] = refs

        print("  Putting shared values...")
        print("    Allocating trefs...")
        params['trefs'] = putsingles(trefs, ctypes.c_float)

        # copy large arrays to ctypes
        print("    Allocating points...")
        params['points'] = RawArray(ctypes.c_float, params['npoints']*3)
        _points = np.ascontiguousarray(points, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(params['npoints']*3):
            params['points'][ind] = _points[ind]

        # make a buffer of time index arrays
        print("    Allocating tinds...")
        params['tinds'] = []
        for ind in range(params['nacqs']):
            params['tinds'].append(RawArray(ctypes.c_int, params['npoints']))
        
        # make a buffer of mask arrays
        print("    Allocating masks...")
        params['masks'] = []
        for ind in range(params['nacqs']):
            params['masks'].append(RawArray(ctypes.c_int, params['npoints']))

        # make a buffer to process data
        print("    Allocating databuffer...")
        params['data'] = RawArray(ctypes.c_float, params['nacqs']*params['nsamp'])

        print("  Registering beamformer with global indexes")
        __BMFRM_PARAMS__[self.id] = params

        print("  Filling tables")
        self.__init_masks__()
        self.__init_tabs__()
    
    def __gen_tab__(self, ind):
        # load parameters
        params = __BMFRM_PARAMS__[self.id]
        npoints = ctypes.c_int(params['npoints'])
        nsamp = ctypes.c_int(params['nsamp'])
        ref = np.ascontiguousarray(params['refs'][ind,:], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
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
        ref = np.ascontiguousarray(params['refs'][ind,:], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        fnum = ctypes.c_float(params['fnum'])
        alpha = float(params['alphas'][ind])
        mask = params['masks'][ind]
        focus = np.ascontiguousarray([np.sin(alpha), 0, np.cos(alpha)], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        norm = np.ascontiguousarray([1, 0, 0], dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        # generate mask
        trig.genmask3D(npoints, fnum, ctypes.c_int(1), fnum, ctypes.c_int(1), norm, focus, ref, params['points'], mask)

    def __init_tabs__(self):
        print("    Generating Transmission Tabs")
        with Pool() as p:
            p.map(self.__gen_tab__, range(__BMFRM_PARAMS__[self.id]['nacqs']))
    
    def __init_masks__(self):
        print("    Generating masks")
        with Pool() as p:
            p.map(self.__gen_mask__, range(__BMFRM_PARAMS__[self.id]['nacqs']))

    def __get_data__(self, ind):
        params = __BMFRM_PARAMS__[self.id]
        npoints = ctypes.c_int(params['npoints'])
        nsamp = ctypes.c_int(params['nsamp'])
        tind = params['tinds'][ind]
        data = params['data']
        indc = ctypes.c_int(ind)

        trig.selectdata(nsamp, npoints, indc, tind, data)
        pass

    def __call__(self, data):
        params = __BMFRM_PARAMS__[self.id]
        nacqs = params['nacqs']
        npoints = params['npoints']
        data = np.ascontiguousarray(data, dtype=ctypes.c_float).ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        for ind in range(params['nacqs'] * params['nsamp']):
            params['data'] = data[ind]

        # send data collection to parallelization pool (eg delay)
        with Pool() as p:
            outputs = p.map(self.__get_data__, range(nacqs))

        # sum up all output vectors and clear from memory(eg and sum)
        summed = outputs[0]
        for ind in range(1, nacqs):
            sumtemp = trig.sumvecs(npoints, summed, outputs[ind], 0)
            trig.freeme(summed)
            trig.freeme(outputs[ind])
            summed = sumtemp

        sumnp = np.array([summed[ind] for ind in range(npoints)], dtype=float)
        trig.freeme(summed)
        return sumnp
        