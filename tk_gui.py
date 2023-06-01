from terrain import *
from visualize_3d_terrain import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

MAX_VAL = 6


def quit_me():
    window.quit()
    window.destroy()


def new_terrain():
    global terrain, button_var
    terrain = Terrain(MAX_VAL)
    visualize_terrain_3d(terrain.square_terrain.mat, button_var.get())
    canvas.draw()


def toggle_button():
    if button_var.get():
        button_var.set(False)
        button.config(text="OFF")
        update_terrain(False)
    else:
        button_var.set(True)
        button.config(text="ON")
        update_terrain(True)


def update_terrain(var):
    global button_var
    var = button_var.get()
    # Retrieve the current values from the sliders
    size = int(size_slider.get())
    smoothness = smoothness_slider.get()
    # Generate the terrain with the updated parameters
    global terrain
    plt.clf()  # Clear the previous plot
    terrain.set_smoothness(smoothness)
    terrain.change_size(sizer=size)
    # Redraw the canvas
    visualize_terrain_3d(terrain.terrain, var)
    canvas.draw()


def update_size_label(value):
    size_label_value.config(text=str(int(float(value))) + ' pow of 2 = ' + str(2 ** int(float(value))))


def update_smoothness_label(value):
    smoothness_label_value.config(text=str(round(float(value), 1)))


# Define the parameters and their initial values
size = 6
smoothness = 0.5
terrain = Terrain(MAX_VAL)

# Create the tkinter window
window = tk.Tk()
window.title("Terrain Generator")
window.protocol("WM_DELETE_WINDOW", quit_me)
window.geometry("1280x720")

# Set grid column weights
for i in range(4):
    window.grid_columnconfigure(i, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=10)

# Create slider for size
size_label = ttk.Label(window, text="Size")
size_label.grid(row=0, column=0)
size_slider = ttk.Scale(window, from_=1, to=MAX_VAL, value=size, orient=tk.HORIZONTAL, variable=tk.IntVar())
size_slider.grid(row=0, column=1, sticky="ew")
# Create a label to display the current value of the size slider
size_label_value = ttk.Label(window)
size_label_value.grid(row=0, column=2)
# Update the size label value when the size slider is moved
size_slider.config(command=lambda value: [update_terrain(value), update_size_label(value)])
# Initial update of the size label value
update_size_label(size_slider.get())

# Create slider for smoothness
smoothness_label = ttk.Label(window, text="Smoothness")
smoothness_label.grid(row=1, column=0)
smoothness_slider = ttk.Scale(window, from_=0, to=2, value=smoothness, orient=tk.HORIZONTAL, variable=tk.DoubleVar())
smoothness_slider.grid(row=1, column=1, sticky="ew")
# Create a label to display the current value of the smoothness slider
smoothness_label_value = ttk.Label(window)
smoothness_label_value.grid(row=1, column=2)
# Update the smoothness label value when the smoothness slider is moved
smoothness_slider.config(command=lambda value: [update_terrain(value), update_smoothness_label(value)])
# Initial update of the smoothness label value
update_smoothness_label(smoothness_slider.get())

# Create a button to generate a new terrain
new_button = ttk.Button(window, text="New Terrain", command=new_terrain)
new_button.grid(row=0, column=3, sticky="ew")

button_var = tk.BooleanVar()
button = tk.Button(window, text="OFF", command=toggle_button)
button.grid(row=1, column=3, sticky="ew")

# Create a blank figure and canvas for Matplotlib plot
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().grid(row=2, columnspan=4, sticky="nsew")

# toolbar = NavigationToolbar2Tk(canvas, window)
# toolbar.update()
# toolbar.grid(row=3)

# Visualize the initial terrain
visualize_terrain_3d(terrain.square_terrain.mat, False)

# Start the tkinter event loop
window.mainloop()
