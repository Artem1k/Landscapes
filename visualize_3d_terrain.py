import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stl import mesh
from mpl_toolkits.mplot3d import Axes3D


# Some animation
def animation_rotate(ax, canvas):
    def animate(i):
        ax.view_init(elev=30, azim=i)
        return figure

    ani = FuncAnimation(figure, animate, frames=360, interval=10, blit=False)
    canvas.draw()


def visualize_terrain_3d(terrain: list, var, canvas, ani_var):
    length = len(terrain) - 1
    plt.clf()
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
    # ax.set_zlim(-0.5, 0.5)
    ax.set_zlim(-7.5, 7.5)
    ax.set_xlim(0, length)
    ax.set_ylim(0, length)

    # ax.set_title('Fractal Terrain')
    if ani_var:
        animation_rotate(ax, canvas)

    canvas.draw()


def visualize_first_terrain_3d(terrain, var, canvas, ani_var):
    terrain_frames = terrain.square_terrain.frames

    def update_figure(i):
        if i == len(terrain_frames):
            if ani_var:
                visualize_terrain_3d(terrain_frames[-1], var, canvas, ani_var)
        else:
            terrain_list = terrain_frames[i]
            visualize_terrain_3d(terrain_list, var, canvas, False)

    animation = FuncAnimation(figure, update_figure, frames=len(terrain_frames) + 1, interval=200, repeat=False)

    canvas.draw()


def export_plot(terrain):
    terrain_array = np.array(terrain)

    # Create a grid of coordinates
    x = np.arange(terrain_array.shape[1])
    y = np.arange(terrain_array.shape[0])
    x_grid, y_grid = np.meshgrid(x, y)

    # Convert the data to mesh representation
    vertices = np.column_stack([x_grid.flatten(), y_grid.flatten(), terrain_array.flatten()])

    # Generate the triangular faces
    rows, cols = terrain_array.shape
    triangles = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            v1 = i * cols + j
            v2 = i * cols + j + 1
            v3 = (i + 1) * cols + j
            v4 = (i + 1) * cols + j + 1
            triangles.append([v1, v2, v3])
            triangles.append([v2, v4, v3])
    triangles = np.array(triangles)

    # Create the mesh object
    mesh_data = mesh.Mesh(np.zeros(triangles.shape[0], dtype=mesh.Mesh.dtype))
    mesh_data.vectors = vertices[triangles]
    mesh_data.update_normals()

    # Save the mesh to an STL file
    mesh_data.save('terrain.stl')


figure = plt.figure()
