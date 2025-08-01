import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

H = 0.5
n_max = 6
length = 2**n_max + 1
step = 2**n_max
half_step = step // 2

x = np.linspace(0, 1, length)
y = x
x, y = np.meshgrid(x, y)
z = np.zeros_like(x)
fig = plt.figure()

ax = fig.add_subplot(111, projection="3d")
# Generate your 3D plot
for n in range(1, n_max + 1):
    rng = 2 ** (-2 * n * H)
    for i in range(0, length - step, step):
        for j in range(0, length - step, step):
            z[i + half_step, j] = (
                0.5 * (z[i, j] + z[i + step, j]) + (1 - 2 * np.random.random()) * rng
            )
            z[i, j + half_step] = (
                0.5 * (z[i, j] + z[i, j + step]) + (1 - 2 * np.random.random()) * rng
            )
            z[i + step, j + half_step] = (
                0.5 * (z[i + step, j] + z[i + step, j + step])
                + (1 - 2 * np.random.random()) * rng
            )
            z[i + half_step, j + step] = (
                0.5 * (z[i, j + step] + z[i + step, j + step])
                + (1 - 2 * np.random.random()) * rng
            )
            z[i + half_step, j + half_step] = (
                0.25
                * (z[i, j] + z[i, j + step] + z[i + step, j] + z[i + step, j + step])
                + (1 - 2 * np.random.random()) * rng
            )

    step = step // 2
    half_step = half_step // 2

    ax.clear()
    ax.plot_surface(x, y, z, cmap="viridis")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(-0.5, 0.5)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    plt.pause(0.2)  # Adjust the pause duration as needed

plt.show()
