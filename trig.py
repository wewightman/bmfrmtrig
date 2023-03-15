import platform as _pltfm
import ctypes

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
pwtxengine = _trig.pwtxengine

_trig.rxengine.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
_trig.rxengine.restype = ctypes.POINTER(ctypes.c_float)
rxengine = _trig.rxengine

_trig.genmask3D.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.c_float, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
_trig.genmask3D.restype = ctypes.POINTER(ctypes.c_int)
genmask3D = _trig.genmask3D

_trig.calcindices.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
calcindices = _trig.calcindices

_trig.selectdata.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float),)
_trig.selectdata.restype = ctypes.POINTER(ctypes.c_float)
selectdata = _trig.selectdata

_trig.sumvecs.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_float)
_trig.sumvecs.restype = ctypes.POINTER(ctypes.c_float)
sumvecs = _trig.sumvecs

_trig.freeme.argtypes = (ctypes.c_void_p,)
freeme = _trig.freeme

_trig.printifa.argtypes = (ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float))
printifa = _trig.printifa
