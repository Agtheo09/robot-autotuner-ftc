import cv2 as cv
import os

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# folderPath = "..\imgs\\sampled"

counter = 1

while True: 
    _, frame = cap.read()

    cv.imshow("View", frame)

    if cv.waitKey(50) == ord("p"):
        cv.imwrite("./imgs/sampled/sample-{0:0=3d}.jpg".format(counter), frame)
        print(counter)
        counter += 1

    if cv.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
cv.destroyAllWindows()