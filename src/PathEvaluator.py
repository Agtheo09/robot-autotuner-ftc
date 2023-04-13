import math
import numpy as np
import numpy as np
from scipy.stats import linregress
from scipy.interpolate import interp1d

class PathEvaluator:
    pathPoints = np.array([]) # [[x1, y1], [x2, y2], [x3, y3], ... [xn, yn]]
    timestamps = np.array([])
    linearity_index = -1
    startStopOffset = []
    
    def __init__(self, pathPoints, timestamps):
        self.pathPoints = pathPoints
        self.timestamps = timestamps
    
    def pathLinearity(self):        
        allX = self.pathPoints[:, 0]
        allY = self.pathPoints[:, 1]
        
        slope, intercept, r_value, p_value, std_err = linregress(allX, allY)
        
        self.linearity_index = r_value**2
        
    def pathInterpolation(self):
        tempX = self.pathPoints[:, 0]
        tempY = self.pathPoints[:, 1]
        
        t_new = np.linspace(min(self.timestamps), max(self.timestamps), 100)

        f1 = interp1d(self.timestamps, tempX, kind='cubic')
        f2 = interp1d(self.timestamps, tempY, kind='cubic')

        x_new = f1(t_new)
        y_new = f2(t_new)
        
        return np.column_stack(x_new, y_new)
    
    
    def startStopError(self):
        lenPoints = len(self.pathPoints)
        self.startStopOffset[0] = math.abs(self.pathPoints[0][0] - self.pathPoints[lenPoints-1][0])
        self.startStopOffset[1] = math.abs(self.pathPoints[0][1] - self.pathPoints[lenPoints-1][1])
        
        return self.startStopOffset