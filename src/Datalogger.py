import csv
import numpy as np
import datetime


class Datalogger:
    headers = ["timestamp", "x", "y", "heading"]

    # Log Files Directory
    directory = "./logs"

    def calculateFullPath(self, filename):
        fullPath = f"{self.directory}/{filename}.csv"

        return fullPath

    def saveExpFile(self, expName, content):
        with open(self.calculateFullPath(expName), "w") as f:
            writer = csv.writer(f)

            writer.writerow(self.headers)
            writer.writerows(content)

    def readCSV(self, filename):
        data = np.genfromtxt(
            f"{self.directory}/{filename}.csv",
            delimiter=",",
            dtype=float,
            skip_header=1,
        )

        return data
