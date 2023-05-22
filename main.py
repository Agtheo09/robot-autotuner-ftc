import cv2 as cv
import numpy as np
from cvzone import FPS

# Custom Classes
from src.Apriltagging import AprilTagging
from src.Localizer import Localizer
from src.PathCapturer import PathCapturer
from src.Datalogger import Datalogger
from src.PathEvaluator import PathEvaluator
from src.CameraCalibrator import CameraCalibrator
from src.WebcamStreaming import WebcamStreaming

if __name__ == "__main__":
    # Capturing Input
    cap = WebcamStreaming(src="./imgs/sample-vid.mp4")
    cap.start()
    # cap = cv.VideoCapture("./imgs/sample-vid.mp4")

    fpsReader = FPS()
    minFPS = 200
    maxFPS = 0
    sumFps = 0
    counter = 0

    # Initializing Custom Classes
    tagDetector = AprilTagging()
    localizer = Localizer(numOfRobotTags=2, tagOffset=np.array([0, 0]))
    datalogger = Datalogger()
    capturer = PathCapturer("Experiment")

    pathCapturerRunning = False

    frame = cap.read()

    tagDetector.update(frame)
    cam_calibr = CameraCalibrator(
        tagDetector.getTagCenterById(localizer.fieldTagIds[0]),
        tagDetector.getTagCenterById(localizer.fieldTagIds[1]),
        tagDetector.getTagCenterById(localizer.fieldTagIds[2]),
        tagDetector.getTagCenterById(localizer.fieldTagIds[3]),
        frame_size=(frame.shape[0], frame.shape[0]),
        padding=50,
    )

    reverted = cam_calibr.applyPerspectiveRevert(frame)

    localizer.updateFieldTagPositions(cam_calibr.getFieldTagPositions())

    tagDetector.update(reverted)

    robotTagPositions = [(0, 0), (0, 0)]

    while cap.isQEmpty():
        # while True:
        frame = cap.read()

        # Calibrating Camera
        calibrated = cam_calibr.applyPerspectiveRevert(frame)

        # Detecting Apriltags
        detectedMat = tagDetector.update(calibrated)

        # Update Tag Positions
        robotTagPositions = list(
            map(
                lambda x: tagDetector.getTagCenterById(x), localizer.robotTagIds
            )
        )

        # Calulate Poses, Velocities etc
        localizer.update(robotTagPositions)

        robotPose = localizer.getRobotPose()
        robotSpeed = localizer.getRobotCurrentVelocity()

        # print(localizer.positioningInstructions())
        print("Pose: ", np.asarray(robotPose))

        capturer.update(robotPose)

        if cv.waitKey(1) == ord("c"):
            # if not capturer.captureEnabled and localizer.atTheCorrectSpot():
            if not capturer.captureEnabled:
                capturer.startCapturing()
        if cv.waitKey(1) == ord("v"):
            if capturer.captureEnabled:
                capturer.stopCapturing()

        rawSize = frame.shape[:2]

        # FPS
        fps, plusFPS = fpsReader.update(
            detectedMat, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
        )

        # FPS Calculations
        minFPS = fps if fps < minFPS else minFPS
        maxFPS = fps if fps > maxFPS else maxFPS
        sumFps += fps
        counter += 1

        # stacked_frames = np.hstack(
        #     (cv.resize(frame, (720, 720)), cv.resize(plusFPS, (720, 720)))
        # )

        # Display the stacked frames
        # cv.imshow("Preview", stacked_frames)
        cv.imshow("Raw", cv.resize(frame, (720, 720)))
        cv.imshow("Proccessed", cv.resize(plusFPS, (700, 700)))
        # cv.imshow("Proccessed", plusFPS)

        if cv.waitKey(5) & 0xFF == 27:
            break

    cap.stop()
    # cap.release()
    cv.destroyAllWindows()
    # FPS Calculations Preview
    print("Max FPS: ", maxFPS)
    print("Min FPS: ", minFPS)
    print("Average FPS: ", sumFps / counter)
