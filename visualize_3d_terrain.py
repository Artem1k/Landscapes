import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


def visualize_terrain_3d(terrain, var, canvas):
    # Convert the terrain data to a NumPy array
    terrain_array = np.array(terrain)

    # Create a grid of coordinates
    x = np.arange(terrain_array.shape[1])
    y = np.arange(terrain_array.shape[0])
    x_grid, y_grid = np.meshgrid(x, y)

    # Create a 3D plot
    ax = figure.add_subplot(111, projection='3d')
    ax.set_position([0, 0, 1, 1])  # Set the position and size of the subplot within the figure
    ax.set_box_aspect([2, 2, 1])

    # Plot the terrain surface using matplotlib's plot_surface function
    ax.plot_surface(x_grid, y_grid, terrain_array, cmap='terrain')

    # Set labels and title, axis and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Elevation')
    ax.set_axis_off()
    if var:
        ax.set_axis_on()
    ax.set_zlim(-0.5, 0.5)

    # Some animation
    # def animate(i):
    #     ax.view_init(elev=20, azim=i*4)
    #     return figure
    # ani = animation.FuncAnimation(figure, animate, frames=90, interval=200, blit=False)

    canvas.draw()
    # ax.set_title('Fractal Terrain')


figure = plt.figure()
