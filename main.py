import cv2 as cv
import numpy as np
import time
import keyboard

# Custom Classes
from src.Apriltagging import AprilTagging
from src.Localizer import Localizer
from src.PathCapturer import PathCapturer
from src.Datalogger import Datalogger
from src.CameraCalibrator import CameraCalibrator
from src.VideoStream import VideoStream

if __name__ == "__main__":
    cap = VideoStream("./imgs/sample-vid.mp4").start()

    # Initializing Custom Classes
    tagDetector = AprilTagging()
    localizer = Localizer(numOfRobotTags=2, tagOffset=np.array([0, 0]))
    datalogger = Datalogger()
    capturer = PathCapturer("Experiment")

    pathCapturerRunning = False

    frame = cap.read()

    tagDetector.update(frame)
    fieldTagsCenters = tagDetector.getTagCentersByIds(localizer.fieldTagIds)
    cam_calibr = CameraCalibrator(
        fieldTagsCenters,
        frame_size=(frame.shape[0], frame.shape[0]),
        padding=50,
    )

    reverted = cam_calibr.applyCalibrations(frame)

    localizer.updateFieldTagPositions(cam_calibr.getFieldTagPositions())

    tagDetector.update(reverted)

    robotTagPositions = [(0, 0), (0, 0)]

    counter = 1
    sumOfFPS = 0
    # while cap.more():
    while True:
        start_time = time.time()
        frame = cap.read()
        if frame is None:
            continue

        # Calibrating Camera
        calibrated = cam_calibr.applyCalibrations(frame)

        # Detecting Apriltags
        detectedMat = tagDetector.update(calibrated)

        # Update Tag Positions
        robotTagPositions = tagDetector.getTagCentersByIds(
            localizer.robotTagIds
        )

        # Calulate Poses, Velocities etc
        localizer.update(robotTagPositions)

        robotPose = localizer.getRobotPose()
        robotVelocity = localizer.getRobotCurrentVelocity()

        # print(localizer.positioningInstructions())
        # print("Pose: ", np.asarray(robotPose))

        capturer.update(robotPose)

        if keyboard.is_pressed("c"):
            # if not capturer.captureEnabled and localizer.atTheCorrectSpot():
            if not capturer.captureEnabled:
                capturer.startCapturing()
        if keyboard.is_pressed("v"):
            if capturer.captureEnabled:
                capturer.stopCapturing()

        dt = time.time() - start_time + 0.000000000000000001
        fps = 1 / dt
        sumOfFPS += fps
        counter += 1
        print("Current FPS: ", fps)
        cv.putText(
            detectedMat,
            f"FPS: {fps}",
            (50, 50),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2,
            cv.LINE_AA,
        )

        # Show Mats
        cv.imshow("Raw", cv.resize(frame, (720, 720)))
        cv.imshow("Proccessed", cv.resize(detectedMat, (700, 700)))

        if cv.waitKey(1) & 0xFF == 27:
            break

    cap.stop()
    # cap.release()
    cv.destroyAllWindows()
    print("Average FPS: ", sumOfFPS / counter)
