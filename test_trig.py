import trig
import numpy as np
from time import time
import matplotlib.pyplot as plt

points = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [-1, 0, 1],
    [0, -1, 1],
    [0, 1, 1],
    [0, 0, 2]
]).astype(float)
print(trig.pwtxengine(1, 0, np.array([0.25, 0.25, 0.25]), np.array([0,0,1]), points))


x = np.linspace(-5, 5, 1000)
y = 0
z = np.linspace(0.1, 10.1, 1000)
X, Y, Z = np.meshgrid(x, y, z)

points = np.array([X.flatten(),Y.flatten(),Z.flatten()]).T

tstart = time()
mask = trig.genmask3D(2, True, 2, True, np.array([1,0,0]), np.array([0, 0, 1]), np.array([0,0,0]), points)
tend = time()
print(mask)
print(tend-tstart)
mask = mask.reshape((X.shape), order='f').squeeze()

plt.figure()
plt.imshow(mask)
plt.show()


