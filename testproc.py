import numpy as np
import PWBeamformer as pwb
import matplotlib.pyplot as plt
import ctypes
import trigc as trig

params = {}
params['points'] = np.arange(3*16).reshape((-1,3))
params['c'] = 1540
params['fnum'] = 2
params['alphas'] = np.array([-0.2, 0.2])
params['trefs']  = 2E-9*np.array([1, 1])
params['refs'] = np.array([[-0.5, 0, 0],[0.5, 0, 0]])
params['ts'] = 1E-8
params['tstart'] = 1.5E-3
params['nsamp'] = 1500

pwb.PWBeamformer(**params)

