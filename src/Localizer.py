import cv2 as cv
import math
import time
import json
import numpy as np


class Localizer:
    # Util
    time1 = 0  # Sec
    time2 = 0  # Sec
    deltaTime = 0  # Sec
    deltaPosition = [0, 0]  # Meters

    pixelsPerMeter = 0

    # Robot Output
    lastRobotPosition = [1, 1]  # Meters
    robotHeading = 0  # Degrees
    robotVelocity = [0.0, 0.0]  # m/s

    def __init__(self, numOfRobotTags=-1, tagOffset=np.array([0, 0])):
        assert (
            numOfRobotTags == 1 or numOfRobotTags == 2 or numOfRobotTags == -1
        )
        self.numOfRobotTags = numOfRobotTags
        self.tagOffset = tagOffset
        self.robotPose = np.array([0.0, 0.0, 0.0])
        self.lastRobotPose = np.array([0.0, 0.0, 0.0])

        # Get Constants
        with open("./src/constants.json") as f:
            constants = json.load(f)

            self.fieldDimension = constants["field"]["sideLength"]

            self.fieldTagIds = [
                constants["tags"]["field"]["topLeft"],
                constants["tags"]["field"]["topRight"],
                constants["tags"]["field"]["bottomLeft"],
                constants["tags"]["field"]["bottomRight"],
            ]
            self.robotTagIds = [
                constants["tags"]["robot"]["left"],
                constants["tags"]["robot"]["right"],
            ]

    def normalize(self, value):
        return value / self.pixelsPerMeter

    def normalizePoint(self, value):
        return [value[0] / self.pixelsPerMeter, value[1] / self.pixelsPerMeter]

    def updateFieldTagPositions(self, fieldTagPositions):
        self.fieldTagPositions = fieldTagPositions
        TLTag = self.fieldTagPositions[0]  # Top Left Tag Position
        TRTag = self.fieldTagPositions[1]  # Top Right Tag Position

        self.pixelsPerMeter = math.dist(TLTag, TRTag) / self.fieldDimension

    def update(self, robotTagPositions):
        if robotTagPositions[0] is None or robotTagPositions[1] is None:
            return self.robotPose

        robotTagPositions = np.array(robotTagPositions)

        if self.numOfRobotTags == 2:
            tagMidPoint = np.mean(robotTagPositions, axis=1)

            # X
            self.robotPose[0] = (
                self.normalize(tagMidPoint[0]) - self.tagOffset[0] / 100
            )

            # Y
            self.robotPose[1] = (
                self.normalize(tagMidPoint[1]) - self.tagOffset[1] / 100
            )

            # # Robot Heading
            self.robotPose[2] = math.degrees(
                math.atan2(
                    robotTagPositions[0][1] - robotTagPositions[1][1],
                    robotTagPositions[1][0] - robotTagPositions[0][0],
                )
            )
        elif self.numOfRobotTags == 1:
            # X
            self.robotPose[0] = (
                self.normalize(robotTagPositions[0][0])
                - self.tagOffset[0] / 100
            )

            # Y
            self.robotPose[1] = (
                self.normalize(robotTagPositions[0][1])
                - self.tagOffset[1] / 100
            )

        self.time2 = time.time()
        self.deltaPosition = (self.robotPose - self.lastRobotPose)[:2]
        print(self.robotPose, self.lastRobotPose)

        self.deltaTime = self.time2 - self.time1

        # self.robotVelocity = math.sqrt(self.deltaPosition[0]**2 + self.deltaPosition[1]**2)/self.deltaTime # if it's for one value
        self.robotVelocity = self.deltaPosition / self.deltaTime

        self.lastRobotPose = self.robotPose
        self.time1 = time.time()

    def getRobotPosition(self):
        return self.robotPose[:2]

    def getRobotPose(self):
        return self.robotPose

    def getRobotHeading(self):
        return self.robotPose[2]

    def getRobotCurrentVelocity(self):
        return self.robotVelocity
