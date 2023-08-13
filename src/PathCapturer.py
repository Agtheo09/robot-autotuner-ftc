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

    # * @param experimentName: Name of the experiment
    def __init__(self, experimentName="Experiment"):
        self.experimentName = experimentName

    def addPoint(self, pose):
        self.timestamp = time() - self.expStartingTime

        # Combine Timestamp and Pose to make a row
        row = np.concatenate((np.array([self.timestamp]), pose.copy()))

        self.rows.append(row)

        self.path.append(pose[:2])

    def startCapturing(self):
        # Reset Meter
        self.path = []
        self.rows = []
        self.expStartingTime = time()

        # Toggle State Machine
        self.captureEnabled = True

    def stopCapturing(self):
        # Toggle State Machine
        self.captureEnabled = False

        # Save Experiment
        dateCode = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        fileName = f"{self.experimentName}_{dateCode}"
        self.datalogger.saveExpFile(fileName, self.rows)

        # Visualize Experiment
        self.visualizer.visualizeExperiments([fileName])

        # Reset Meter
        self.path = []

    # * @param pose: New Pose that is added to the sequence(x, y, theta)
    def update(self, pose):
        if self.captureEnabled:
            self.addPoint(pose)
