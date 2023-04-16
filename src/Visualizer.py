import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Visualizer:
    pointHistory = []
    xs = []
    ys = []
    
    fieldDimension = 10
    
    def __init__(self):
        pass
    
    def liveVisualize(self, newPoint):
        lenOfHistory = len(self.pointHistory)
        lastX, lastY = self.pointHistory[lenOfHistory-1]
        
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
            
    
    
    def endVisualize(self, paths, labelNames, animate, animInterval):
        max_length = max(len(path) for path in paths)
        n = len(paths)
        xs = []
        ys = []
        
        pathNames = []
        
        if not labelNames:
            for i in range(n):
                pathNames.append(f'Path {i}')
        else:
            pathNames = labelNames

        for path in paths:
            tempX = []
            tempY = []
            for point in path:
                tempX.append(point[0])
                tempY.append(point[1])
            
            xs.append(tempX)
            ys.append(tempY)
        
        if animate:
            fig, ax = plt.subplots()

            lines = [ax.plot([], [], color='green', linewidth=2, zorder=5)[0] for i in range(n)]
            scats = [ax.scatter([], [], marker='.', color='yellow', zorder=10) for i in range(n)]

            padding = 0;
                
            ax.set_xlim(padding, self.fieldDimension+padding)
            ax.set_ylim(padding, self.fieldDimension+padding)

            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            def animateNonLive(i):
                for j in range(n):
                    curX = xs[j]
                    curY = ys[j]
                    
                    lines[j].set_data(curX[:i+1], curY[:i+1])
                    scats[j].set_offsets(np.c_[curX[:i+1], curY[:i+1]])
                
                return tuple(scats) + tuple(lines)

            ani = animation.FuncAnimation(fig, animateNonLive, frames=max_length, interval=animInterval, blit=True)

            plt.title('Robot Position')
            plt.show()
        else:
            for i in range(len(xs)):
                xPoints = xs[i]
                yPoints = ys[i]
                
                plt.plot(xPoints, yPoints, label=pathNames[i])
                plt.scatter(xPoints, yPoints, marker='.', color='red', zorder=10)

            plt.legend()
            plt.show()