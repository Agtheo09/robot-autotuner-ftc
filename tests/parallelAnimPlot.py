import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fieldDimension = 10

paths = [
    [[0, 0], [1, 2], [4, 1], [5, 8], [2, 2]],
    [[1, 1], [2, 3], [5, 2], [6, 9], [3, 3]],
    [[2, 2], [3, 4], [6, 3], [7, 10], [4, 4]]
]

names = ['Path 1', 'Path 2']

max_length = max(len(path) for path in paths)

n = len(paths)

xs = []
ys = []

for path in paths:
    tempX = []
    tempY = []
    for point in path:
        tempX.append(point[0])
        tempY.append(point[1])
    
    xs.append(tempX)
    ys.append(tempY)
    
fig, ax = plt.subplots()

lines = [ax.plot([], [], color='green', linewidth=2, zorder=5)[0] for i in range(n)]
scats = [ax.scatter([], [], marker='.', color='yellow', zorder=10) for i in range(n)]

padding = 0;
    
ax.set_xlim(padding, fieldDimension+padding)
ax.set_ylim(padding, fieldDimension+padding)

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

def animate(i):
    for j in range(n):
        curX = xs[j]
        curY = ys[j]
        
        lines[j].set_data(curX[:i+1], curY[:i+1])
        scats[j].set_offsets(np.c_[curX[:i+1], curY[:i+1]])
    
    return tuple(scats) + tuple(lines)

# Set frames to the length of any of the tempX or tempY lists
ani = animation.FuncAnimation(fig, animate, frames=max_length, interval=200, blit=True)

plt.title('Robot Position')
plt.show()

# for i in range(len(xs)):
#     xPoints = xs[i]
#     yPoints = ys[i]
    
#     print(names[i])
#     plt.plot(xPoints, yPoints, label=names[i])
#     plt.scatter(xPoints, yPoints, marker='.', color='red', zorder=10)

# plt.legend()
# plt.show()