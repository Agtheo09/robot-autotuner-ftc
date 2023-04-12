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
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


fieldTagIds = [100, 101, 102, 103] # Top Left, Top Right, Bottom Left, Bottom Right
robotTagIds = [104, 105] # Left, Right

# Robot Outputs
robotPose = [0, 0, 0] # X, Y, Heading

# Initializing Custom Classes
tagDetector = AprilTagging()
localizer = Localizer(2, [0, 0])
datalogger = Datalogger()
capturer = PathCapturer("Test")

# Field Tag Positions
fieldTagPoints = []

# Temp Variables
matrix = None
rows = None

pathCapturerRunning = False

def calculatePerspectiveMatrix(frame, april1, april2, april3, april4):
    global matrix
    global rows
    global fieldTagPoints
    rows = frame.shape[0]

    originalPos = np.float32([april1, april2, april3, april4])
    dist = 20
    fieldTagPoints = np.float32([[dist,dist],[rows-dist,dist],[dist, rows-dist],[rows-dist,rows-dist]])

    matrix = cv.getPerspectiveTransform(originalPos, fieldTagPoints)
    
def applyPerspectiveRevert(frame):
    result = cv.warpPerspective(frame.copy(), matrix, (rows, rows))

    # Scaling
    # height, width = result.shape[:2]
    # scaled = cv.resize(result, (int(width * 2), int(height * 2)))

    return result


_, frame = cap.read()

tagDetector.update(frame)
calculatePerspectiveMatrix(frame,
                           tagDetector.getTagCenterById(fieldTagIds[0]),
                           tagDetector.getTagCenterById(fieldTagIds[1]),
                           tagDetector.getTagCenterById(fieldTagIds[2]),
                           tagDetector.getTagCenterById(fieldTagIds[3]))

reverted = applyPerspectiveRevert(frame)

tagDetector.update(reverted)

# fieldTagPoints = list(map(lambda x : tagDetector.getTagCenterById(x), fieldTagIds)) # Fields

while True:
    _, frame = cap.read()
    
    reverted = applyPerspectiveRevert(frame)
    
    # Detecting Apriltags
    detectedMat = tagDetector.update(reverted)

    # Update Tag Positions
    robotTagPositions = list(map(lambda x : tagDetector.getTagCenterById(x), robotTagIds)) # Robot

    # print(robotTagPositions)
    if robotTagPositions[0] is not None and robotTagPositions[1] is not None:
        localizer.update(fieldTagPoints, robotTagPositions)
        currentPosition = localizer.getRobotPosition()
        robotPose[0] = currentPosition[0]
        robotPose[1] = currentPosition[1]
        robotPose[2] = localizer.getRobotHeading()
        
        if pathCapturerRunning:
            # print("Capturing...")
            capturer.update(robotPose)
        
        if cv.waitKey(1) == ord('c'):
            if not pathCapturerRunning:
                pathCapturerRunning = True
                capturer.startCapturing()
        if cv.waitKey(1) == ord('v'):
            if pathCapturerRunning:
                pathCapturerRunning = False
                capturer.stopCapturing()

    cv.imshow("Raw", frame)
     # height, width = result.shape[:2]
    cv.imshow("Output", detectedMat)
    
    if cv.waitKey(5) & 0xFF == 27:
        break

cv.waitKey(0)
cv.destroyAllWindows()
