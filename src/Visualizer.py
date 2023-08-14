import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from .Datalogger import Datalogger


class Visualizer:
    pointHistory = []

    # Log Files Directory
    directory = "./logs"

    HIDE_AXIS = False

    plot_colors = [
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
    ]

    # * @param fieldDim: Tuple of (x, y) dimenssion
    def __init__(self, fieldDim=(3.6, 3.6)):
        self.fileReader = Datalogger()
        self.fieldDimension = fieldDim

    # * @param newPoint: Tuple of (x, y, θ)
    def liveVisualize(self, newPoint):
        lenOfHistory = len(self.pointHistory)
        lastX, lastY = self.pointHistory[lenOfHistory - 1]

        self.positionChanged = newPoint[0] != lastX or newPoint[1] != lastY

        fig, ax = plt.subplots()

        def update(i):
            if self.positionChanged:
                self.pointHistory.append(newPoint)
                x_lst, y_lst = zip(*self.pointHistory)
                self.xs = list(x_lst)
                self.ys = list(y_lst)

                ax.clear()
                ax.plot(self.xs, self.ys)

        # Create the animation
        ani = animation.FuncAnimation(fig, update, interval=100)

        # Show the plot
        plt.show()

    # * @param expNames: List of Experiment names
    # * @param labelNames: List of Labels for the experiments
    # * @param animate: If True, the animation will be shown
    # * @param animInterval: Interval between frames in milliseconds
    # * @param viewPts: If True, the points will be shown
    def visualizeExperiments(
        self,
        expNames,
        labelNames=None,
        animate=True,
        animInterval=10,
        viewPts=False,
    ):
        xs = []
        ys = []

        for exp in expNames:
            curData = self.fileReader.readCSV(f"{exp}")

            tempX = []
            tempY = []
            for row in curData:
                tempX.append(row[1])
                tempY.append(row[2])

            xs.append(tempX)
            ys.append(tempY)

        pathNames = []
        n = len(expNames)
        max_length = max(len(sublist) for sublist in xs)

        if labelNames == None:
            for i in range(1, n + 1):
                pathNames.append(f"Path {i}")
        else:
            pathNames = labelNames

        if animate:
            fig, ax = plt.subplots()

            lines = [
                ax.plot(
                    [],
                    [],
                    color=self.plot_colors[i],
                    linewidth=2,
                    zorder=i + 2,
                    label=pathNames[i],
                )[0]
                for i in range(n)
            ]
            scats = [
                ax.scatter([], [], marker=" ", color="yellow", zorder=15)
                for i in range(n)
            ]

            padding = 0

            ax.set_xlim(
                -self.fieldDimension[0] - padding,
                self.fieldDimension[0] + padding,
            )
            ax.set_ylim(
                -self.fieldDimension[1] - padding,
                self.fieldDimension[1] + padding,
            )

            ax.set_aspect("equal")

            # Move Axis to the center
            ax.spines["left"].set_position("center")
            ax.spines["bottom"].set_position("center")
            ax.spines["right"].set_color("none")
            ax.spines["top"].set_color("none")

            if self.HIDE_AXIS:
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)

            # It works but i dont know how
            def animateNonLive(i):
                for j in range(n):
                    curX = xs[j]
                    curY = ys[j]

                    lines[j].set_data(curX[: i + 1], curY[: i + 1])
                    if viewPts:
                        scats[j].set_offsets(
                            np.c_[curX[: i + 1], curY[: i + 1]]
                        )

                return tuple(scats) + tuple(lines)

            ani = animation.FuncAnimation(
                fig,
                animateNonLive,
                frames=max_length,
                interval=animInterval,
                blit=True,
            )

            plt.title("Experiments" if len(expNames) > 1 else "Experiment")
            plt.legend()
            plt.show()
        else:
            for i in range(len(xs)):
                xPoints = xs[i]
                yPoints = ys[i]

                plt.plot(xPoints, yPoints, label=pathNames[i])
                plt.scatter(
                    xPoints, yPoints, marker=".", color="red", zorder=10
                )

            plt.legend()
            plt.show()
