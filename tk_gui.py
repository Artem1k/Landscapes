import time

from terrain import *
import tkinter as tk
from tkinter import ttk

MAX_VAL = 10


def update_terrain():
    # Retrieve the current values from the sliders
    size = int(size_slider.get())
    smoothness = round(smoothness_slider.get(), 1)

    # Generate the terrain with the updated parameters
    global terrain
    # terrain = generate_terrain(size, smoothness)
    plt.clf()  # Clear the previous plot
    # visualize_terrain_3d(terrain)  # Visualize the updated terrain
    terrain.set_smoothness(sm=smoothness)
    terrain.visualize(sizer=size)

    plt.draw()  # Redraw the figure
    # Update the visualization with the new terrain


# Create the tkinter window
window = tk.Tk()
window.title("Terrain Generator")

# Define the parameters and their initial values

size = 7
smoothness = 0.5

# Create sliders for width, height, and smoothness
size_label = ttk.Label(window, text="size")
size_label.pack()
size_slider = ttk.Scale(window, from_=1, to=MAX_VAL, value=size, orient=tk.HORIZONTAL, variable=tk.IntVar())
size_slider.pack()

smoothness_label = ttk.Label(window, text="Smoothness")
smoothness_label.pack()
smoothness_slider = ttk.Scale(window, from_=0.5, to=2, value=smoothness, orient=tk.HORIZONTAL, variable=tk.IntVar())
smoothness_slider.pack()

# Create a button to update the terrain
update_button = ttk.Button(window, text="Update Terrain", command=update_terrain)
update_button.pack()

# Create a terrain
# terrain = GenerateTerrain(MAX_VAL)
# terrain.iterate()
# figure = Terrain(square_terrain=terrain)

terrain = Terrain(MAX_VAL)
# Visualize the terrain in 3D
terrain.visualize(sizer=size)

# Start the tkinter event loop
window.mainloop()
