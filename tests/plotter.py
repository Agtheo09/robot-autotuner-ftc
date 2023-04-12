import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

data = np.genfromtxt("./tests/values_2.csv", delimiter = ',', dtype=float, skip_header=1)
bg = plt.imread("./imgs/powerplay-field.png")

# print(data)

x = []
y = []

fieldDimension = 1.495
    
for row in data:
    x.append(row[1])
    y.append(row[2])
    
fig, ax = plt.subplots()
scat = ax.scatter([], [], marker='.', color='blue')
line, = ax.plot([], [], color='black', alpha=0.5)

def animate(i):
    line.set_data(x[:i+1], y[:i+1])
    scat.set_offsets(np.c_[x[:i+1], y[:i+1]])
    
    padding = 0;
    
    ax.set_xlim(padding, fieldDimension+padding)
    ax.set_ylim(padding, fieldDimension+padding)
    
    # ax.set_xlim(min(x)-padding, max(x)+padding)
    # ax.set_ylim(min(y)-padding, max(y)+padding)
    
    ax.imshow(bg, extent=[padding, fieldDimension+padding, padding, fieldDimension+padding])
    
    return scat, line,

# plt.plot(x, y)
# plt.scatter(x, y, marker='.', color='red')
# plt.xlim([0, 1.6])
# plt.ylim([0, 1.6])
# plt.xlabel('X')
# plt.ylabel('Y')

ani = animation.FuncAnimation(fig, animate, frames=len(x), interval=20, blit=True)

plt.title('Robot Position')
plt.show()