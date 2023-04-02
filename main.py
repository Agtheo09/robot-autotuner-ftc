import cv2 as cv
from pupil_apriltags import Detector
import numpy as np

# Custom Classes
from src.classes.Apriltagging import AprilTagging
from src.classes.Localizer import Localizer
from src.classes.PathCapturer import PathCapturer
from src.classes.Datalogger import Datalogger
from src.classes.PathEvaluator import PathEvaluator


# Capturing Input
img = cv.imread("./imgs/test-input.jpg")
img = cv.resize(img, (680, 680))


fieldTagIds = [100, 101, 102, 103] # Top Left, Top Right, Bottom Left, Bottom Right
robotTagIds = [104, 105] # Left, Right

# Robot Outputs
# Smth here

# Initializing Custom Classes
tagDetector = AprilTagging()
localizer = Localizer(2, [0, 0])

# Detecting Apriltags
tagDetector.update(img)

# Update Tag Positions
fieldTagPositions = list(map(lambda x : tagDetector.getTagById(x).center, fieldTagIds)) # Field
# robotTagPositions = list(map(lambda x : tagDetector.getTagById(x).center, robotTagIds)) # Robot

cv.imshow("Result", img)
# cv.imwrite("outputimg.png", img)

cv.waitKey(0)
cv.destroyAllWindows()
