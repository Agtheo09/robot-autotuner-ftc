import cv2 as cv
import numpy as np
from pupil_apriltags import Detector

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

tagsDetected = None
tags = [] # (26, 41), (469, 28), (144, 428), (413, 425)
detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0,
)


def detectApriltags(input):
    global tags
    grayscaleImage = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
    tagsDetected = detector.detect(grayscaleImage)

    tempTags = []

    for tag in tagsDetected:
        tempTags.append(tag)

        ptA, ptB, ptC, ptD = tag.corners

        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))

        cv.line(input, ptA, ptB, (255, 0, 0), 2)
        cv.line(input, ptB, ptC, (255, 0, 0), 2)
        cv.line(input, ptC, ptD, (255, 0, 0), 2)
        cv.line(input, ptD, ptA, (255, 0, 0), 2)

        cv.putText(
            input,
            str(tag.tag_id),
            (ptB[0] + 10, ptB[1] + 15),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv.LINE_AA,
        )

    tags = tempTags


def perspectiveRevert(frame, april1, april2, april3, april4):
    rows, cols, ch = frame.shape

    pts1 = np.float32([april1, april2, april3, april4])
    dist = 80
    fieldTagPoints = np.float32(
        [
            [dist, dist],
            [rows - dist, dist],
            [dist, rows - dist],
            [rows - dist, rows - dist],
        ]
    )

    matrix = cv.getPerspectiveTransform(pts1, fieldTagPoints)
    result = cv.warpPerspective(frame, matrix, (rows, rows))
    padding = 15
    y = int(fieldTagPoints[0][1]) - padding
    h = int(fieldTagPoints[3][1]) + padding
    x = int(fieldTagPoints[0][0]) - padding
    w = int(fieldTagPoints[3][0]) + padding
    result = result[y:h, x:w]
    print("After: ", result.shape)

    height, width = result.shape[:2]

    scaled = cv.resize(result, (int(width * 2), int(height * 2)))

    return scaled


while True:
    _, frame = cap.read()
    # cv.rotate(frame, cv.ROTATE_180)

    # Detecting Apriltags
    detectApriltags(frame)

    reverted = perspectiveRevert(
        frame,
        tags[0],
        tags[1],
        tags[2],
        tags[3],
    )
    cv.imshow("Reverted View", reverted)

    cv.imshow("Raw View", frame)

    if cv.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()
