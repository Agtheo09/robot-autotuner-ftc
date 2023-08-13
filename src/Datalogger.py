import csv
import numpy as np
import datetime
import os


class Datalogger:
    headers = ["timestamp", "x", "y", "heading"]

    # * @param directory: Directory to save the log files
    def __init__(self, directory="./logs"):
        # Log Files Directory
        self.directory = directory

    # * @param filename: Filename of the log file
    def calculateFullPath(self, filename):
        return os.path.join(self.directory, f"{filename}.csv")

    # * @param expName: Name of the experiment
    # * @param content: Content of the log file ["timestamp", "x", "y", "heading"]
    def saveExpFile(self, expName, content):
        with open(self.calculateFullPath(expName), "w") as f:
            writer = csv.writer(f)

            writer.writerow(self.headers)
            writer.writerows(content)

    # * @param filename: Filename of the log file
    def readCSV(self, filename):
        data = np.genfromtxt(
            os.path.join(self.directory, f"{filename}.csv"),
            delimiter=",",
            dtype=float,
            skip_header=1,
        )

        return data
