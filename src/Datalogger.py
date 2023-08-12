import csv
import numpy as np
import datetime
import os


class Datalogger:
    headers = ["timestamp", "x", "y", "heading"]

    # Log Files Directory
    directory = "./logs"

    def calculateFullPath(self, filename):
        return os.path.join(self.directory, f"{filename}.csv")

    def saveExpFile(self, expName, content):
        with open(self.calculateFullPath(expName), "w") as f:
            writer = csv.writer(f)

            writer.writerow(self.headers)
            writer.writerows(content)

    def readCSV(self, filename):
        data = np.genfromtxt(
            os.path.join(self.directory, f"{filename}.csv"),
            delimiter=",",
            dtype=float,
            skip_header=1,
        )

        return data
