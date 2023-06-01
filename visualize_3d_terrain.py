import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def visualize_terrain_3d(terrain, var):
    # Convert the terrain data to a NumPy array
    terrain_array = np.array(terrain)

    # Create a grid of coordinates
    x = np.arange(terrain_array.shape[1])
    y = np.arange(terrain_array.shape[0])
    X, Y = np.meshgrid(x, y)

    # Create a 3D plot
    ax = figure.add_subplot(111, projection='3d')

    # Plot the terrain surface using Matplotlib's plot_surface function
    ax.plot_surface(X, Y, terrain_array, cmap='terrain')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Elevation')
    ax.set_axis_off()
    if var:
        ax.set_axis_on()
    # ax.set_title('Fractal Terrain')


figure = plt.figure()
