import math
import cv2 as cv
from pupil_apriltags import Detector

# Custom Classes
from Apriltagging import AprilTagging
from Localizer import Localizer

img = cv.imread("./imgs/apriltag-localization-test-input-low-res.png")


fieldTagIds = [100, 101, 102, 103] # Top Left, Top Right, Bottom Left, Bottom Right
robotTagIds = [104, 105] # Left, Right

# Robot Outputs
# Smth here

# Initializing Custom Classes
tagDetector = AprilTagging()
localizer = Localizer(2, [0, 0])

# Detecting Apriltags
tagDetector.update(input)
        
# Update Tag Positions
fieldTagPositions = list(map(lambda x : tagDetector.getTagById(x).center, fieldTagIds)) # Field
robotTagPositions = list(map(lambda x : tagDetector.getTagById(x).center, robotTagIds)) # Robot

cv.imshow("Result", img)
# cv.imwrite("outputimg.png", img)

cv.waitKey(0)
cv.destroyAllWindows()
