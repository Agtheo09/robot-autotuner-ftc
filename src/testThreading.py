from VideoStream import WebcamStreaming
from cvzone import FPS
import cv2 as cv
import time

# cap = WebcamStreaming(src="./imgs/sample-vid.mp4")
# cap.start()
cap = cv.VideoCapture("./imgs/sample-vid.mp4")

fpsReader = FPS()
minFPS = 200
maxFPS = 0
sumFps = 0
counter = 0

time.sleep(3)

# while cap.isQEmpty():
while True:
    frame = cap.read()[1]

    # FPS
    fps, plusFPS = fpsReader.update(
        frame.copy(), pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
    )

    minFPS = fps if fps < minFPS else minFPS
    maxFPS = fps if fps > maxFPS else maxFPS
    sumFps += fps
    counter += 1

    cv.imshow("Output", plusFPS)

    if cv.waitKey(5) & 0xFF == 27:
        break

# cap.stop()
cap.release()
cv.destroyAllWindows()
print("Max FPS: ", maxFPS)
print("Min FPS: ", minFPS)
print("Average FPS: ", sumFps / counter)
