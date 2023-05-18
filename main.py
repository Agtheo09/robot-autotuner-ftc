import cv2 as cv
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
    cap = cv.VideoCapture("./imgs/sample-vid.mp4")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    # cap = WebcamStreaming(src="./imgs/sample-vid.mp4")
    # cap.start()

    fpsReader = FPS()
    minFPS = 200
    maxFPS = 0

    # Initializing Custom Classes
    tagDetector = AprilTagging()
    localizer = Localizer(numOfRobotTags=2, tagOffset=[0, 0])
    datalogger = Datalogger()
    capturer = PathCapturer("Experiment")

    pathCapturerRunning = False

    frame = cap.read()[1]
    # frame = cap.read()

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

    while True:
        frame = cap.read()[1]
        # frame = cap.read()

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

        localizer.update(robotTagPositions)

        robotPose = localizer.getRobotPose()
        robotSpeed = localizer.getRobotCurrentVelocity()

        print("Pose: ", robotPose, "  Velocity: ", robotSpeed)

        capturer.update(robotPose)

        if cv.waitKey(1) == ord("c"):
            if not capturer.captureEnabled and localizer.atTheCorrectSpot():
                capturer.startCapturing()
        if cv.waitKey(1) == ord("v"):
            if capturer.captureEnabled:
                capturer.stopCapturing()

        rawSize = frame.shape[:2]
        cv.imshow("Raw", cv.resize(frame, (720, 720)))
        # height, width = result.shape[:2]

        # FPS
        fps, plusFPS = fpsReader.update(
            detectedMat, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
        )

        minFPS = fps if fps < minFPS else minFPS
        maxFPS = fps if fps > maxFPS else maxFPS

        cv.imshow("Output", cv.resize(plusFPS, (720, 720)))

        if cv.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    # cap.stop()
    cv.destroyAllWindows()
    print("Max FPS: ", maxFPS)
    print("Min FPS: ", minFPS)
