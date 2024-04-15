import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def f(s, p):
    """Create a python function, f,  with the following behavior:

    the function, f,  takes two inputs, s and p. the range for s is 0 to 1. the range for p is -2 to +2.  The function f(s,p) increases with either s or p increasing. The function should have the following constraints: f(1,-2) == f(.5, 0) == f(0,2) and f(0.5, -2) == f(0.25, -1) == f(0, 0).
    """
    # Define the scaling factors for s and p
    scale_s = 4  # default to stated range of p
    scale_p = 1  # default to stated range of 2

    # Calculate the base value for the constraints, e.g. f(1,-2) == f(0.5, 0) == f(0,2)
    # base_value = scale_s * 0.5 + scale_p * 0.0  # default to mid-points of stated ranges
    base_value = scale_s * 0.5 + scale_p * 0  # default to mid-points of stated ranges

    # Adjust the function to increase with either s or p increasing
    return (scale_s * s + scale_p * p + base_value) / (scale_s + scale_p + base_value)


def plot_score():
    # Create a grid of x and y values
    s = np.linspace(0, 1, 100)
    p = np.linspace(-2, 2, 100)
    s, p = np.meshgrid(s, p)

    # Calculate z values based on the function
    z = f(s, p)

    # Create a figure and a 3D axis
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection="3d")

    # Plot the surface
    ax.plot_surface(s, p, z, cmap="viridis", alpha=0.5)
    ax.contour3D(s, p, z, cmap="viridis", offset=0.0)

    # Set labels and show the plot
    ax.set_xlabel("Surprisingness")
    ax.set_ylabel("Preference")
    ax.set_zlabel("Score")
    plt.show(block=True)


if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>> in main")
    plot_score()
