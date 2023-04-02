import cv2 as cv
import math
import time

class Localizer:
    numOfRobotTags = -1
    
    # Constants
    tagOffset = [0, 0] # X, Y CM
    fieldDimension = 3.65 # Meters
    pixelsPerMeter = 0
    
    fieldTagPositions = []
    robotTagPositions = []
    
    # Util
    time1 = 0 # Sec
    time2 = 0 # Sec
    deltaTime = 0 # Sec
    deltaPosition = [0, 0]
    
    # Robot Output
    robotPosition = [0, 0]
    lastRobotPosition = [1, 1]
    robotHeading = 0
    robotVelocity = 0
    
    def __init__(self, numOfRobotTags, tagOffset):
        assert(numOfRobotTags == 1 or numOfRobotTags == 2)
        self.numOfRobotTags = numOfRobotTags
        self.tagOffset = tagOffset
        
    
    def normalize(self, value):
        return value / self.pixelsPerMeter
    
    def update(self, fieldTgPositions, robotTgPositions):        
        self.fieldTagPositions = fieldTgPositions
        self.robotTagPositions = robotTgPositions
        
        TLTag = self.fieldTagPositions[0] # Top Left Tag Position
        TRTag = self.fieldTagPositions[1] # Top Right Tag Position
        self.pixelsPerMeter = math.sqrt((TLTag[0] - TRTag[0])**2 + (TLTag[1] - TRTag[1])**2) / self.fieldDimension
        
        if self.numOfRobotTags == 2:
            # Robot Position
            self.robotPosition[0] = self.normalize(
                (self.robotTagPositions[0][0] + self.robotTagPositions[1][0]) / 2) - self.tagOffset[0]/100
            self.robotPosition[1] = self.normalize(
                (self.robotTagPositions[0][1] + self.robotTagPositions[1][1]) / 2) - self.tagOffset[1]/100
            
            self.time2 = time.time()
            self.deltaPosition[0] = self.robotPosition[0] - self.lastRobotPosition[0]
            self.deltaPosition[1] = self.robotPosition[1] - self.lastRobotPosition[1]
            self.deltaTime = self.time2 - self.time1
            # self.robotVelocity = math.sqrt(self.deltaPosition[0]**2 + self.deltaPosition[1]**2)/self.deltaTime # if it's for one value
            self.robotVelocity[0] = self.deltaPosition[0]/self.deltaTime
            self.robotVelocity[1] = self.deltaPosition[1]/self.deltaTime
            
            # Robot Heading
            self.robotHeading = math.degrees(math.atan2(
                self.robotTagPositions[0][1] - self.robotTagPositions[1][1],
                self.robotTagPositions[1][0] - self.robotTagPositions[0][0]))
        elif self.numOfRobotTags == 1:
            self.robotPosition[0] = self.normalize(
                self.robotTagPositions[0][0]) - self.tagOffset[0]/100
            self.robotPosition[1] = self.normalize(
                self.robotTagPositions[0][1]) - self.tagOffset[1]/100
            
        self.lastRobotPosition = self.robotPosition
        self.time1 = time.time()
        
    def getRobotPosition(self):
        return self.robotPosition
    
    def getRobotHeading(self):
        return self.robotHeading
    
    def getRobotCurrentVelocity(self):
        return self.robotVelocity