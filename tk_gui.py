from terrain import *
from visualize_3d_terrain import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAX_VAL = 6


def update_terrain():
    # Retrieve the current values from the sliders
    size = int(size_slider.get())
    smoothness = round(smoothness_slider.get(), 1)

    # Generate the terrain with the updated parameters
    global terrain
    plt.clf()  # Clear the previous plot
    terrain.set_smoothness(smoothness)
    terrain.change_size(sizer=size)
    visualize_terrain_3d(terrain.square_terrain.mat)
    # Redraw the canvas
    canvas.draw()


def quit_me():
    print('quit')
    window.quit()
    window.destroy()


# Create the tkinter window
window = tk.Tk()
window.title("Terrain Generator")
window.protocol("WM_DELETE_WINDOW", quit_me)
# Define the parameters and their initial values
size = 6
smoothness = 0.5

terrain = Terrain(MAX_VAL)

# Create sliders for width, height, and smoothness
size_label = ttk.Label(window, text="Size")
size_label.pack()
size_slider = ttk.Scale(window, from_=1, to=MAX_VAL, value=size, orient=tk.HORIZONTAL, variable=tk.IntVar())
size_slider.pack()

smoothness_label = ttk.Label(window, text="Smoothness")
smoothness_label.pack()
smoothness_slider = ttk.Scale(window, from_=0, to=2, value=smoothness, orient=tk.HORIZONTAL, variable=tk.DoubleVar())
smoothness_slider.pack()

# Create a button to update the terrain
update_button = ttk.Button(window, text="Update Terrain", command=update_terrain)
update_button.pack()

# Create a blank figure and canvas for Matplotlib plot
# figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack()

# Visualize the initial terrain
visualize_terrain_3d(terrain.square_terrain.mat)

# Start the tkinter event loop
window.mainloop()
