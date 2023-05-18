import cv2 as cv
from WebcamStreaming import WebcamStreaming
from cvzone import FPS

cap = WebcamStreaming(src="./imgs/sample-vid.mp4")

cap.start()

# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()

fpsReader = FPS()
minFPS = 200
maxFPS = 0

while True:
    frame = cap.read()

    fps, plusFPS = fpsReader.update(
        frame, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
    )

    minFPS = fps if fps < minFPS else minFPS
    maxFPS = fps if fps > maxFPS else maxFPS

    cv.imshow("View", plusFPS)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.stop()
cv.destroyAllWindows()
print("Max FPS: ", maxFPS)
print("Min FPS: ", minFPS)
