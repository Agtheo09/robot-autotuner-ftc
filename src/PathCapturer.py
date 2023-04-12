import numpy as np
from .Datalogger import Datalogger
from time import time

class PathCapturer:
    rows = []
    path = []
    captureEnabled = False
    experimentName = ""
    expStartingTime = None
    timestamp = None

    datalogger = Datalogger()
    
    def __init__(self, experimentName):
        self.experimentName = experimentName

    def addPoint(self, pose):
        self.timestamp = time() - self.expStartingTime
        row = [0, 0, 0, 0]
        
        row[0] = self.timestamp
        row[1] = pose[0]
        row[2] = pose[1]
        row[3] = pose[2]
        
        self.rows.append(row)
        
        self.path.append(pose[:2])

    def startCapturing(self):
        self.path = []
        self.rows = []
        self.captureEnabled = True
        self.expStartingTime = time()

    def stopCapturing(self):
        self.captureEnabled = False
        self.datalogger.saveExpFile(self.experimentName, self.rows)
        self.path = []
 
    def update(self, pose):            
        if self.captureEnabled:
            print("Passed: ", self.path)
            self.addPoint(pose)
            