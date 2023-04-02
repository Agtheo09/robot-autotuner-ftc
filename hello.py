import numpy as np
from scipy.interpolate import interp1d

# Define the known points
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 3, 2, 5, 1])

# Define the range of points to interpolate
x_new = np.linspace(0, 4, 10)

# Create an interpolation function
f = interp1d(x, y, kind='cubic')

# Use the interpolation function to generate the missing points
y_new = f(x_new)

# Print the interpolated points
print(y_new)