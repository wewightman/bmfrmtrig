import bmfrm.trigengines as trig
from multiprocessing import Pool
import numpy as np

global POINTS
global C
global TS
global TSTART
global NSAMP
global FNUM
global TINDS
global MASKS
global SLICE

class PWBeamformer():
    """"""
    def __init__(self, c, ts, tstart, nsamp:int, fnum, points, refs, trefs, alphas):
        global POINTS
        global C
        global TS
        global TSTART
        global NSAMP
        global FNUM
        POINTS = points
        C = c
        TS = ts
        TSTART = tstart
        NSAMP = nsamp
        FNUM = fnum
        self.refs = refs
        self.trefs = trefs
        self.alphas = alphas
        self.tinds = []

        print("Initializing tabs")
        self.__init_tabs__()
        print("Initializing Masks")
        self.__init_masks__()
    
    def gentabs(self, ind):
        tau_rx = trig.rxengine(C, self.refs[ind,:], POINTS)
        tau_tx = trig.pwtxengine(C, self.trefs[ind], self.alphas[ind], 0, self.refs[ind,:], POINTS)
        return np.round((tau_rx + tau_tx - TSTART)/TS).astype(int)

    def __init_tabs__(self):
        global TINDS
        with Pool() as p:
            TINDS = p.map(self.gentabs, range(len(self.trefs)))

    def genmasks(self, ind):
        tau_rx = trig.rxengine(C, self.refs[ind,:], POINTS)
        return ind*np.ones(tau_rx.shape)

    def __init_masks__(self):
        pass

    def bmfrm(self, ind):
        return SLICE[TINDS[ind], ind]
    
    def __call__(self, data):
        global SLICE
        SLICE = data
        print("Shape:", SLICE.shape)
        print("Tinds shape", len(TINDS), TINDS[0].shape)

        with Pool() as p:
            results = p.map(self.bmfrm, range(len(self.trefs)))
        
        print(len(results), results[0].shape)
        print(results[0])
        print(TINDS[0])
        summed = 0
        for result in results:
            summed += result
        return summed