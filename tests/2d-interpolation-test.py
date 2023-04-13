import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

t = np.arange(1, 20+1)
x = np.sort(np.random.rand(20)) * 20
y = np.random.uniform(0, 100, 20)

print(min(x), len(x))

t_new = np.linspace(min(t), max(t), 300)

f1 = interp1d(t, x, kind='cubic')
f2 = interp1d(t, y, kind='cubic')

x_new = f1(t_new)
y_new = f2(t_new)

plt.plot(x, y)
plt.plot(x_new, y_new)
plt.legend(["Raw", "Interpolated"])
plt.show()