import numpy as np
from Datalogger import Datalogger

class PathCapturer:
    path = np.array([])
    captureEnabled = False
    experimentName = ""

    # datalogger = Datalogger()
    
    def __init__(self, experimentName):
        self.experimentName = experimentName

    def addPoint(self, point):
        self.path.append(point)

    def startCapturing(self):
        self.captureEnabled = True

    def stopCapturing(self):
        self.captureEnabled = False
        # self.datalogger.saveExpFile(self.experimentName, self.path)
        self.path = np.array([])
 
    def update(self, point):            
        if self.captureEnabled:
            self.addPoint(point)