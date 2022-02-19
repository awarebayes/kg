import numpy as np

points = np.zeros((400, 2))
s = np.ones((points.shape[0], 1))
points = np.hstack([points, s])
print(points)