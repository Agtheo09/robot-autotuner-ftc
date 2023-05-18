import cv2 as cv
import numpy as np


class CameraCalibrator:
    def __init__(
        self,
        topLeft,
        topRight,
        bottomLeft,
        bottomRight,
        frame_size=(1080, 1080),
        padding=20,
    ):
        self.padding = padding
        self.frame_size = frame_size
        # desired fieldTagPositions
        self.fieldTagPositions = np.float32(
            [
                [self.padding, self.padding],
                [self.frame_size[0] - self.padding, self.padding],
                [self.padding, self.frame_size[1] - self.padding],
                [
                    self.frame_size[0] - self.padding,
                    self.frame_size[1] - self.padding,
                ],
            ]
        )

        self.updateCorners(topLeft, topRight, bottomLeft, bottomRight)

    def updateCorners(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.originalPos = np.float32(
            [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
        )
        self.perspective_matrix = cv.getPerspectiveTransform(
            self.originalPos, self.fieldTagPositions
        )

    def getFieldTagPositions(self):
        return self.fieldTagPositions

    def applyPerspectiveRevert(self, frame):
        return cv.warpPerspective(
            frame.copy(),
            self.perspective_matrix,
            self.frame_size,
        )
