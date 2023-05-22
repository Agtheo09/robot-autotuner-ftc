import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from .Datalogger import Datalogger


class Visualizer:
    pointHistory = []

    fieldDimension = (3.6, 3.6)

    # Log Files Directory
    directory = "./logs"

    def __init__(self):
        self.fileReader = Datalogger()

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
            for i in range(n):
                pathNames.append(f"Path {i}")
        else:
            pathNames = labelNames

        if animate:
            fig, ax = plt.subplots()

            lines = [
                ax.plot([], [], color="green", linewidth=2, zorder=5)[0]
                for i in range(n)
            ]
            scats = [
                ax.scatter([], [], marker=" ", color="yellow", zorder=10)
                for i in range(n)
            ]

            padding = 0

            # ax.set_xlim(padding, self.fieldDimension + padding)
            # ax.set_ylim(padding, self.fieldDimension + padding)
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

            # ax.get_xaxis().set_visible(False)
            # ax.get_yaxis().set_visible(False)

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

            plt.title("Experiments") if len(expNames) > 1 else plt.title(
                "Experiment"
            )
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
