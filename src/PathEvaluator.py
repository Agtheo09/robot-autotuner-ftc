import math
import numpy as np
import numpy as np
from scipy.stats import linregress
from scipy.interpolate import interp1d

from .Datalogger import Datalogger


class PathEvaluator:
    pathPoints = np.array([])  # [[x1, y1], [x2, y2], [x3, y3], ... [xn, yn]]
    timestamps = np.array([])
    headings = np.array([])

    linearity_index = -1
    startStopOffset = []

    # Log Files Directory
    directory = "./logs"

    def __init__(self, timestamps=np.array([]), pathPoints=np.array([])):
        self.pathPoints = pathPoints
        self.timestamps = timestamps

        self.datalogger = Datalogger()

    def updateDataFromLog(self, expName):
        curData = self.datalogger.readCSV(expName)

        tempTimeStamps = []
        tempPath = []
        tempHeadings = []

        for row in curData:
            tempTimeStamps.append(row[0])
            tempPath.append([row[1], row[2]])
            tempHeadings.append(row[3])

        self.timestamps = np.array(tempTimeStamps)
        self.pathPoints = np.array(tempPath)
        self.headings = np.array(tempHeadings)

    def pathLinearity(self):
        allX = self.pathPoints[:, 0]
        allY = self.pathPoints[:, 1]

        slope, intercept, r_value, p_value, std_err = linregress(allX, allY)

        self.linearity_index = r_value**2

    def pathInterpolation(self, expName):
        tempX = self.pathPoints[:, 0]
        tempY = self.pathPoints[:, 1]

        t_new = np.linspace(min(self.timestamps), max(self.timestamps), 100)

        f1 = interp1d(self.timestamps, tempX, kind="cubic")
        f2 = interp1d(self.timestamps, tempY, kind="cubic")

        x_new = f1(t_new)
        y_new = f2(t_new)

        rows = []

        for i in range(0, len(t_new) - 1):
            rows.append([t_new[i], x_new[i], y_new[i], self.headings[i]])

        self.datalogger.saveExpFile(expName, rows)

        return np.column_stack((x_new, y_new))

    def startStopError(self):
        lenPoints = len(self.pathPoints)
        # self.startStopOffset[0] = math.abs(
        #     self.pathPoints[0][0] - self.pathPoints[lenPoints - 1][0]
        # )
        # self.startStopOffset[1] = math.abs(
        #     self.pathPoints[0][1] - self.pathPoints[lenPoints - 1][1]
        # )
        self.startStopOffset = np.abs(
            self.pathPoints[0] - self.pathPoints[lenPoints - 1]
        )

        return self.startStopOffset
