import cv2
import numpy as np

# Define the set of points
points = np.array([(50,50), (100, 150), (150, 200), (200, 150), (250, 100)], np.float32)

# Create a Line Segment Detector object
lsd = cv2.createLineSegmentDetector()

# Fit a spline to the points
_, _, _, _, vps = lsd.detect([points])

# Draw the spline
img = np.zeros((300, 300, 3), np.uint8)
for i in range(len(vps)):
    cv2.line(img, (int(vps[i][0]), int(vps[i][1])), (int(vps[i][2]), int(vps[i][3])), (0, 255, 0), 3)

# Show the result
cv2.imshow('Spline', img)
cv2.waitKey(0)