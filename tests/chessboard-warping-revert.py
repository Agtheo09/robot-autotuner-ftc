import cv2 as cv
import numpy as np

number_of_squares_X = 10 # Number of chessboard squares along the x-axis
number_of_squares_Y = 7  # Number of chessboard squares along the y-axis
nX = number_of_squares_X - 1 # Number of interior corners along x-axis
nY = number_of_squares_Y - 1 # Number of interior corners along y-axis
square_size = 0.024 # Length of the side of a square in meters

# Store vectors of 3D points for all chessboard images (world coordinate frame)
object_points = []
 
# Store vectors of 2D points for all chessboard images (camera coordinate frame)
image_points = []
 
# Set termination criteria. We stop either when an accuracy is reached or when
# we have finished a certain number of iterations.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# Define real world coordinates for points in the 3D coordinate frame
# Object points are (0,0,0), (1,0,0), (2,0,0) ...., (5,8,0)
object_points_3D = np.zeros((nX * nY, 3), np.float32)       
 
# These are the x and y coordinates                                              
object_points_3D[:,:2] = np.mgrid[0:nY, 0:nX].T.reshape(-1, 2) 
 
object_points_3D = object_points_3D * square_size

inputImage = cv.imread("./warp-input-imgs/sample-000.jpg")

gray = cv.cvtColor(inputImage, cv.COLOR_BGR2GRAY)
# gray = inputImage

cv.imshow("Input Image", inputImage)

success, corners = cv.findChessboardCorners(gray, (nY, nX), None)
print(success)
if success == True:
    print("run")

    # Append object points
    object_points.append(object_points_3D)

    # Find more exact corner pixels       
    corners_2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)       

    # Append image points
    image_points.append(corners_2)

    # Draw the corners
    cv.drawChessboardCorners(inputImage, (nY, nX), corners_2, success)
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_points, 
                                                image_points, 
                                                gray.shape[::-1], 
                                                None, 
                                                None)
    
    height, width = inputImage.shape[:2]
    optimal_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, 
                                                        (width,height), 
                                                        1, 
                                                        (width,height))
    toUndistort = cv.imread("./warp-input-imgs/sample-001.jpg")
    undistorted_image = cv.undistort(inputImage, mtx, dist, None, 
                                optimal_camera_matrix)
    cv.imwrite("./output/outputImg.jpg", undistorted_image)

cv.waitKey(0)