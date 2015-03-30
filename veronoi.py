import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

points = np.array([(0.0,0.0),(5.0,0.0),(5.0,6.0),(10.0,6.0),(10.0,10.0),(0.0,10.0)])
vor = Voronoi(points)

#plot it
voronoi_plot_2d(vor)
plt.show()