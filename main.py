import cv2 as cv
from pupil_apriltags import Detector
import numpy as np

# Custom Classes
from src.Apriltagging import AprilTagging
from src.Localizer import Localizer
from src.PathCapturer import PathCapturer
from src.Datalogger import Datalogger
from src.PathEvaluator import PathEvaluator


# Capturing Input
# cap = cv.VideoCapture(1)

# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()


fieldTagIds = [100, 101, 102, 103] # Top Left, Top Right, Bottom Left, Bottom Right
robotTagIds = [104, 105] # Left, Right

# Robot Outputs
# Smth here

# Initializing Custom Classes
tagDetector = AprilTagging()
localizer = Localizer(2, [0, 0])
datalogger = Datalogger()

# Field Tag Positions
fieldTagPoints = np.array([])

# Temp Variables
matrix = None
rows = None

def calculatePerspectiveMatrix(frame, april1, april2, april3, april4):
    global matrix
    global rows
    global fieldTagPoints
    rows = frame.shape[0]

    originalPos = np.float32([april1, april2, april3, april4])
    dist = 80
    fieldTagPoints = np.float32([[dist,dist],[rows-dist,dist],[dist, rows-dist],[rows-dist,rows-dist]])

    matrix = cv.getPerspectiveTransform(originalPos, fieldTagPoints)
    
def applyPerspectiveRevert(frame):
    result = cv.warpPerspective(frame, matrix, (rows, rows))
    
    # Cropping
    padding = 15
    y = int(fieldTagPoints[0][1]) - padding
    h = int(fieldTagPoints[3][1]) + padding
    x = int(fieldTagPoints[0][0]) - padding
    w = int(fieldTagPoints[3][0]) + padding
    result = result[y:h, x:w]

    # Scaling
    height, width = result.shape[:2]
    scaled = cv.resize(result, (int(width * 2), int(height * 2)))
    
    # return scaled
    return result


# _, frame = cap.read()
frame = cv.imread("./imgs/sampled/sample-002.jpg")

tagDetector.update(frame)
calculatePerspectiveMatrix(frame,
                           tagDetector.getTagCenterById(fieldTagIds[0]),
                           tagDetector.getTagCenterById(fieldTagIds[1]),
                           tagDetector.getTagCenterById(fieldTagIds[2]),
                           tagDetector.getTagCenterById(fieldTagIds[3]))

inputImg = applyPerspectiveRevert(frame)

tagDetector.update(inputImg)

fieldTagPoints = list(map(lambda x : tagDetector.getTagCenterById(x), fieldTagIds)) # Field

# while True:
    # _, frame = cap.read()
    
# Detecting Apriltags
inputImg = tagDetector.update(inputImg)

# Update Tag Positions
robotTagPositions = list(map(lambda x : tagDetector.getTagCenterById(x), robotTagIds)) # Robot

# print(robotTagPositions)
if robotTagPositions[0] is not None and robotTagPositions[1] is not None:
    print("Localizer Running")
    localizer.update(fieldTagPoints, robotTagPositions)
    print(localizer.getRobotPosition())

cv.imshow("Raw", frame)
cv.imshow("Result", inputImg)

cv.waitKey(0)

exit()
    
#     if cv.waitKey(5) & 0xFF == 27:
#         break

# cv.waitKey(0)
# cv.destroyAllWindows()
