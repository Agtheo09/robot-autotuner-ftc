import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

data = np.genfromtxt(
    "./tests/Test_20230510224748643.csv",
    delimiter=",",
    dtype=float,
    skip_header=1,
)
bg = plt.imread("./imgs/powerplay-field.png")

x = []
y = []

fieldDimension = 3.6

for row in data:
    x.append(row[1])
    y.append(row[2])

fig, ax = plt.subplots()

(line,) = ax.plot([], [], color="green", linewidth=2, zorder=5)
scat = ax.scatter([], [], marker=".", color="yellow", zorder=10)

print(x)


def animate(i):
    line.set_data(x[: i + 1], y[: i + 1])
    scat.set_offsets(np.c_[x[: i + 1], y[: i + 1]])

    padding = 0

    ax.set_xlim(padding, fieldDimension + padding)
    ax.set_ylim(padding, fieldDimension + padding)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # ax.imshow(bg, extent=[padding, fieldDimension+padding, padding, fieldDimension+padding])

    return (
        scat,
        line,
    )


ani = animation.FuncAnimation(
    fig, animate, frames=len(x), interval=20, blit=True
)

plt.title("Robot Position")
plt.show()
