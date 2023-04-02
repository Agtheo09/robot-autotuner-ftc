import cv2 as cv

img = cv.imread("./imgs/apriltag-localization-test-input-low-res.png")

# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

cv.imshow("Result", img)

cv.waitKey(0)
cv.destroyAllWindows()
