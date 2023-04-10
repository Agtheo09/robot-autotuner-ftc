import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Define the known points
x = np.array([0, 1, 2, 3, 5])
y = np.array([0, 3, 1, 5, 1])

# Define the range of points to interpolate
x_new = np.linspace(0, 5, 100)

# Create an interpolation function
f = interp1d(x, y, kind='cubic')

# Use the interpolation function to generate the missing points
y_new = f(x_new)

# Print the interpolated points
plt.plot(x, y)
plt.plot(x_new, y_new)
plt.legend(["Raw", "Interpolated"])
plt.show()