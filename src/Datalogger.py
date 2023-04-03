import numpy as np
import csv
import datetime

class Datalogger:
    # headers = ["timestamp", "x", "y", "heading"]
    headers = ["x", "y", "heading"]
    directory = "./logs"
    
    def calculateFullPath(self, expName):
        milliseconds = datetime.datetime.now().microsecond
        curTime = str(int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+round(milliseconds/1000000, 3))
        fullPath = f"{self.directory}/{expName}_{curTime}.csv"
        
        return fullPath
    
    def saveExpFile(self, expName, content):
        with open(self.calculateFullPath(expName), "w") as f:
            writer = csv.writer(f)
            
            writer.writerow(self.headers)
            writer.writerows(content)
            