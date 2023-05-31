import random
import matplotlib.pyplot as plt


def generate_landscape(size, h):
    landscape = [0 for _ in range(size)]

    step_size = size - 1
    half_step = step_size // 2
    n = 1

    while step_size > 1:
        ranged = pow(2, -2 * n * h)
        for i in range(0, size - step_size - 1, step_size):
            landscape[i + half_step] = 0.5 * (landscape[i] + landscape[i + step_size]) + (
                        1 - 2 * random.random()) * ranged
        step_size = half_step
        half_step = step_size // 2
        n += 1
        # Here is code to visualize each step of iterations
        # plt.plot(range(size), landscape, linewidth=2)
        # plt.axis([0, size - 1, -0.5, 0.5])
        # plt.axis('off')
        # plt.show(block=False)
        # plt.pause(0.5)
        # plt.clf()
    return landscape


def visualize_landscape(landscape):
    size = len(landscape)
    x = range(size)
    y = [landscape[i] for i in range(size)]

    plt.plot(x, y)
    plt.title("2D Landscape Visualization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis([x[0], x[-1], -0.5, 0.5])
    plt.axis('off')
    plt.show()


# Generate landscape
size = 33  # Should be a power of 2 plus 1 (e.g., 9, 17, 33, ...)
roughness = 0.8
landscape = generate_landscape(size, roughness)

# Visualize landscape
visualize_landscape(landscape)

# It is also code for each step visualization, but then comment a visualize_landscape
# plt.show()
