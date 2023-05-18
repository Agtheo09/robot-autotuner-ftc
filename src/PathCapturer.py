import datetime
from time import sleep
import numpy as np
from .Datalogger import Datalogger
from .Visualizer import Visualizer
from time import time


class PathCapturer:
    rows = []
    path = []
    captureEnabled = False
    experimentName = ""
    expStartingTime = None
    timestamp = None

    datalogger = Datalogger()
    visualizer = Visualizer()

    def __init__(self, experimentName):
        self.experimentName = experimentName

    def addPoint(self, pose):
        self.timestamp = time() - self.expStartingTime

        row = np.concatenate((np.array([self.timestamp]), pose.copy()))

        self.rows.append(row)

        self.path.append(pose[:2])

    def startCapturing(self):
        self.path = []
        self.rows = []
        self.captureEnabled = True
        self.expStartingTime = time()

    def stopCapturing(self):
        self.captureEnabled = False
        dateCode = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        fileName = f"{self.experimentName}_{dateCode}"
        self.datalogger.saveExpFile(fileName, self.rows)
        self.visualizer.visualizeExperiments([fileName])
        self.path = []

    def update(self, pose):
        if self.captureEnabled:
            self.addPoint(pose)
