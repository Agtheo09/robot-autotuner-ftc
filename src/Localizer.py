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

    pixelsPerMeter = 0.0

    # Robot Output
    lastRobotPosition = [1, 1]  # Meters
    robotHeading = 0  # Degrees
    robotVelocity = [0.0, 0.0]  # m/s

    poseMaxErrorAllowed = np.array([0.01, 0.01, 1.0])  # Meters, Meters, Degrees

    def __init__(
        self,
        numOfRobotTags=-1,
        tagOffset=np.array([0, 0]),
        startingPose=np.array([0.0, 0.0, 0.0]),
        viewportSize=(1080, 1080),
    ):
        assert (
            numOfRobotTags == 1 or numOfRobotTags == 2 or numOfRobotTags == -1
        )
        self.numOfRobotTags = numOfRobotTags
        self.tagOffset = tagOffset
        self.robotPose = np.array([0.0, 0.0, 0.0])
        self.lastRobotPose = np.array([0.0, 0.0, 0.0])
        self.startingPose = startingPose
        self.viewportSize = viewportSize
        np.set_printoptions(suppress=True)

        # Get Constants
        with open("./src/constants.json") as f:
            constants = json.load(f)

            self.fieldDimension = np.array(
                [
                    constants["field"]["width"],
                    constants["field"]["height"],
                ]
            )

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

    def updateFieldTagPositions(self, fieldTagPositions):
        self.fieldTagPositions = fieldTagPositions
        TLTag, TRTag = self.fieldTagPositions[:2]  # Top Left, Top Right Tag Pos

        self.pixelsPerMeter = math.dist(TLTag, TRTag) / self.fieldDimension[0]
        self.fieldCenter = self.fieldDimension / 2

    def update(self, robotTagPositions):
        if robotTagPositions[0] is None or robotTagPositions[1] is None:
            return self.robotPose

        robotTagPositions = np.array(
            robotTagPositions - self.fieldTagPositions[0]
        )

        if self.numOfRobotTags == 2:
            tagMidPoint = np.mean(robotTagPositions, axis=0)

            self.robotPose[:2] = (
                (self.normalize(tagMidPoint) - self.tagOffset / 100)
                - self.fieldCenter
            ) * np.array([1, -1])

            """ Above, we substract the center of the field in order to set the 
            center of the field as the origin. Then we multiply by [1, -1] in 
            order to flip the y-axis but not the x-axis. This because in OpenCV 
            the y-axis is flipped(- up, + down) """

            # Robot Heading
            #            /  y2 - y1  \
            # θ = arctan| ---------- |
            #           \   x2 - x1 /
            self.robotPose[2] = math.degrees(
                math.atan2(
                    robotTagPositions[0][1] - robotTagPositions[1][1],
                    robotTagPositions[1][0] - robotTagPositions[0][0],
                )
            )
        elif self.numOfRobotTags == 1:
            self.robotPose[:2] = (
                (self.normalize(robotTagPositions[0]) - self.tagOffset / 100)
                - self.fieldCenter
            ) * np.array([1, -1])

        self.time2 = time.time()

        self.calculateRobotVelocity()

        self.lastRobotPose = self.robotPose
        self.time1 = time.time()

    def calculateRobotVelocity(self):
        self.deltaPosition = (self.robotPose - self.lastRobotPose)[:2]
        self.deltaTime = self.time2 - self.time1
        self.robotVelocity = self.deltaPosition / self.deltaTime

    def getRobotPosition(self):
        return self.robotPose[:2]

    def getRobotPose(self):
        return self.robotPose

    def getRobotHeading(self):
        return self.robotPose[2]

    def getRobotCurrentVelocity(self):
        return self.robotVelocity

    def placementOffset(self):
        return self.startingPose - self.robotPose

    def atTheCorrectSpot(self):
        return np.all(self.placementOffset() < self.poseMaxErrorAllowed)

    def positioningInstructions(self):
        return (
            "Ready" if self.atTheCorrectSpot() else str(self.placementOffset())
        )
