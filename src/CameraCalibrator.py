import cv2 as cv
import numpy as np


class CameraCalibrator:
    def __init__(
        self,
        tagCenters,  # Should be in a form of TopLeft, TopRight, BottomLeft, BottomRight
        frame_size=(1080, 1080),
        padding=20,
        fish_eye_enabled=False,
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

        self.fish_eye_enabled = fish_eye_enabled

        self.updateCorners(
            tagCenters[0], tagCenters[1], tagCenters[2], tagCenters[3]
        )
        # Load the fish-eye distortion parameters
        # self.camera_matrix = np.load("camera_matrix.npy")
        # self.dist_coeffs = np.load("distortion_coeffs.npy")

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

    def undistortFrame(self, frame):
        return cv.undistort(frame.copy(), self.camera_matrix, self.dist_coeffs)

    def applyCalibrations(self, frame):
        rawMat = frame.copy()
        # Perspective Revert if Enabled
        inputMat = (
            self.undistortFrame(rawMat) if self.fish_eye_enabled else rawMat
        )

        return cv.warpPerspective(
            inputMat,
            self.perspective_matrix,
            self.frame_size,
        )
