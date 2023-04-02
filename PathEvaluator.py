import numpy as np
import numpy as np
from scipy.stats import linregress

class PathEvaluator:
    pathPoints = np.array([]) # [[x1, y1], [x2, y2], [x3, y3], ... [xn, yn]]
    linearity_index = -1
    
    def __init__(self, pathPoints):
        self.pathPoints = pathPoints
    
    def pathLinearity(self):        
        allX = self.pathPoints[:, 0]
        allY = self.pathPoints[:, 1]
        
        slope, intercept, r_value, p_value, std_err = linregress(allX, allY)
        
        self.linearity_index = r_value**2
        
    def pathInterpolation(self):
        pass
    
    
    def startStopError(self):
        pass