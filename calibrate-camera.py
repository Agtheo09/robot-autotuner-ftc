import cv2 as cv
import numpy as np
import glob

pattern_size = (9, 6)  # Number of internal corners in the chessboard pattern

object_points = []
image_points = []

object_corners = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
object_corners[:, :2] = np.mgrid[
    0 : pattern_size[0], 0 : pattern_size[1]
].T.reshape(-1, 2)

# Path to calibration images folder
calibration_images_folder = "imgs/calibration/"
imgsType = "jpg"

calibration_image_paths = glob.glob(f"{calibration_images_folder}*.{imgsType}")

for img_path in calibration_image_paths:
    img = cv.imread(img_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, pattern_size, None)

    if ret:
        object_points.append(object_corners)
        image_points.append(corners)

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
    object_points, image_points, gray.shape[::-1], None, None
)

# Save the calibration parameters
np.save("camera_matrix.npy", camera_matrix)
np.save("distortion_coeffs.npy", dist_coeffs)
