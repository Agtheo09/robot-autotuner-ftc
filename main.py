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
cap = cv.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


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
    
    return scaled


_, frame = cap.read()

tagDetector.update(frame)
calculatePerspectiveMatrix(frame,
                           tagDetector.getTagCenterById(100),
                           tagDetector.getTagCenterById(101),
                           tagDetector.getTagCenterById(102),
                           tagDetector.getTagCenterById(103))


while True:
    _, frame = cap.read()
    
    inputImg = applyPerspectiveRevert(frame)
    # Detecting Apriltags
    tagDetector.update(inputImg)

    # Update Tag Positions
    # fieldTagPositions = list(map(lambda x : tagDetector.getTagById(x).center, fieldTagIds)) # Field
    robotTagPositions = list(map(lambda x : tagDetector.getTagCenterById(x), robotTagIds)) # Robot

    cv.imshow("Raw", frame)
    cv.imshow("Result", inputImg)
    
    if cv.waitKey(5) & 0xFF == 27:
        break

cv.waitKey(0)
cv.destroyAllWindows()
