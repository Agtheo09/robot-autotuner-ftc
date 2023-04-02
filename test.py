from Apriltagging import AprilTagging
from Localizer import Localizer
from Datalogger import Datalogger
from PathEvaluator import PathEvaluator
import cv2 as cv
import numpy as np
import time

image = cv.imread("./outputimg.png")

pointsTest = np.array([[1, 2], [2, 4], [3, 6], [4, 8], [5, 10]])

foo = AprilTagging()
doo = Localizer(2, [0, 0])
joo = Datalogger()
yoo = PathEvaluator(pointsTest)

testContent = np.array([[1.6, 2.3, 20], [2.6, 4.7, 40], [1.4, 0.8, 60], [6.6, 3.3, 80], [1.1, 2.2, 100], [6.9, 4.2, 120]])

yoo.pathLinearity()

cv.imshow("Input", image)

while(1):
    k = cv.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue

exit()