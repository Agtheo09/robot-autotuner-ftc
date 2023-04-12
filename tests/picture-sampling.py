import cv2 as cv
import os

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# folderPath = "..\imgs\\sampled"

counter = 1

while True: 
    _, frame = cap.read()

    cv.imshow("View", frame)
    
    
    print(cv.waitKey(1) == ord("c"))

    if cv.waitKey(1) == ord("p"):
        cv.imwrite("./imgs/sampled/sample-{0:0=3d}.jpg".format(counter), frame)
        print(counter)
        counter += 1

    if cv.waitKey(1) & 0xFF == 27:
        break
    
cap.release()
cv.destroyAllWindows()