import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Visualizer:
    points = np.array([])
    fieldDimension = 1.495
    x = np.array([])
    y = np.array([])
    
    def __init__(self):
        pass
    
    def updatePoints(self, points):
        self.points = points
        self.x = self.points[:, 0]
        self.y = self.points[:, 1]
    
    
    def endVisualize(self):
        def animate(i):
            line.set_data(self.x[:i+1], self.y[:i+1])
            scat.set_offsets(np.c_[self.x[:i+1], self.y[:i+1]])
            
            padding = 0;
            
            ax.set_xlim(padding, self.fieldDimension+padding)
            ax.set_ylim(padding, self.fieldDimension+padding)
            
            # ax.set_xlim(min(x)-padding, max(x)+padding)
            # ax.set_ylim(min(y)-padding, max(y)+padding)
            
            ax.imshow(bg, extent=[padding, self.fieldDimension+padding, padding, self.fieldDimension+padding])
            
            return scat, line,
        
        bg = plt.imread("./imgs/powerplay-field.png")
        
        fig, ax = plt.subplots()
        scat = ax.scatter([], [], marker='.', color='green')
        line, = ax.plot([], [], color='black', alpha=0.5)

        ani = animation.FuncAnimation(fig, animate, frames=len(self.x), interval=20, blit=True)

        plt.title('Robot Position')
        plt.show()