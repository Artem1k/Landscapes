from terrain import *
from visualize_3d_terrain import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

MAX_VAL = 8


def quit_me():
    window.quit()
    window.destroy()


def new_terrain():
    global out_terrain
    out_terrain = Terrain(MAX_VAL)
    visualize_first_terrain_3d(out_terrain, var=button_var.get(), canvas=canvas, ani_var=button_animation_var.get())


def toggle_button():
    if button_var.get():
        button_var.set(False)
        button.config(text="AXIS_OFF")
        update_terrain(False)
    else:
        button_var.set(True)
        button.config(text="AXIS_ON")
        update_terrain(True)


def anima_button():
    if button_animation_var.get():
        button_animation_var.set(False)
        button_animation.config(text="ANI_OFF")
        update_terrain(False)
    else:
        button_animation_var.set(True)
        button_animation.config(text="ANI_ON")
        update_terrain(True)


def update_terrain_smoothness(var):
    # Generate the terrain with the updated parameters
    out_terrain.set_smoothness(smoothness_slider.get())
    update_terrain(True)


def update_terrain(var):
    var = button_var.get()
    ani_var = button_animation_var.get()
    new_size = int(size_slider.get())
    out_terrain.change_size(sizer=new_size)
    visualize_terrain_3d(out_terrain.updated_terrain, var=var, canvas=canvas, ani_var=ani_var)


def update_size_label(value):
    sizer = 2 ** int(float(value))
    size_label_value.config(text=f'{str(int(float(value)))} pow of 2 = ({sizer}+1)*({sizer}+1) = {str(sizer ** 2)}')


def update_smoothness_label(value):
    smoothness_label_value.config(text=str(round(float(value), 2)))


# Define the parameters and their initial values
size = 5
smoothness = 0.5
out_terrain = Terrain(MAX_VAL)
out_terrain.change_size(size)

# Create the tkinter window
window = tk.Tk()
window.title("Terrain Generator")
window.protocol("WM_DELETE_WINDOW", quit_me)
window.geometry("1000x700")

# Set grid columns weights
for i in range(4):
    window.grid_columnconfigure(i, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=10)

# Create a slider for size
size_label = ttk.Label(window, text="Size")
size_label.grid(row=0, column=0)
size_slider = ttk.Scale(window, from_=0, to=MAX_VAL, value=size, orient=tk.HORIZONTAL,
                        command=lambda value: [update_terrain(value), update_size_label(value)])
size_slider.grid(row=0, column=1, sticky="ew")
# Create a label to display the current value of the size slider
size_label_value = ttk.Label(window)
size_label_value.grid(row=0, column=2)
# Initial update of the size label value
update_size_label(size_slider.get())

# Create a slider for smoothness
smoothness_label = ttk.Label(window, text="Smoothness")
smoothness_label.grid(row=1, column=0)
smoothness_slider = ttk.Scale(window, from_=0, to=2, value=smoothness, orient=tk.HORIZONTAL,
                              command=lambda value: [update_terrain_smoothness(value), update_smoothness_label(value)])
smoothness_slider.grid(row=1, column=1, sticky="ew")
# Create a label to display the current value of the smoothness slider
smoothness_label_value = ttk.Label(window)
smoothness_label_value.grid(row=1, column=2)
# Initial update of the smoothness label value
update_smoothness_label(smoothness_slider.get())

# Create a button to generate a new terrain
new_button = ttk.Button(window, text="New Terrain", command=new_terrain)
new_button.grid(row=0, column=3, sticky="nsew")

# Button for setting axis ON/OFF
button_var = tk.BooleanVar()
button = tk.Button(window, text="AXIS_OFF", command=toggle_button)
button.grid(row=1, column=3, sticky="nsew")

# Create a blank figure and canvas for Matplotlib plot
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().grid(row=2, columnspan=4, sticky="nsew")

toolbarFrame = tk.Frame(master=window)
toolbarFrame.grid(row=3, columnspan=3, sticky="nsew")
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
toolbar.update()
toolbar.pack(side=tk.LEFT)

# Button for setting axis ON/OFF
button_animation_var = tk.BooleanVar(value=True)
button_animation = tk.Button(window, text="ANI_ON", command=anima_button)
button_animation.grid(row=3, column=3, sticky="nsew")

# Visualize the initial terrain
visualize_first_terrain_3d(terrain=out_terrain, var=False, canvas=canvas, ani_var=True)

# Start the tkinter event loop
window.mainloop()
