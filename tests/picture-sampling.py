import time
import cv2 as cv
import os
from cvzone import FPS

# cap = cv.VideoCapture("./imgs/sample-vid.mp4")
cap = cv.VideoCapture("./imgs/sample-vid.mp4")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# folderPath = "..\imgs\\sampled"

counter = 1

fpsReader = FPS()
minFPS = 200
maxFPS = 0


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x, y)


while True:
    _, frame = cap.read()

    # cv.setMouseCallback("View", draw_circle)

    # cv.imwrite("./imgs/sampled/sample-{0:0=3d}.jpg".format(counter), frame)
    # counter += 1

    fps, plusFPS = fpsReader.update(
        frame, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
    )

    cv.imshow("View", cv.resize(plusFPS, (720, 720)))

    minFPS = fps if fps < minFPS else minFPS
    maxFPS = fps if fps > maxFPS else maxFPS

    time.sleep(1 / 30)

    if cv.waitKey(1) & 0xFF == 27:
        break

print("Max FPS: ", maxFPS)
print("Min FPS: ", minFPS)
cv.destroyAllWindows()
