import cv2 as cv
import numpy as np
import time
import keyboard
from matplotlib import pyplot as plt

# Custom Classes
from src.Apriltagging import AprilTagging
from src.Localizer import Localizer
from src.PathCapturer import PathCapturer
from src.Datalogger import Datalogger
from src.CameraCalibrator import CameraCalibrator
from src.VideoStream import VideoStream
from src.Units import DistUnit, AngleUnit

if __name__ == "__main__":
    ##--------------- Initializing Custom Classes & Utilities ----------------##

    cap = VideoStream("./imgs/sample-vid.mp4").start()  # Starting Video Stream
    # cap = VideoStream(0).start() # For Webcam

    # Custom Classes
    tagDetector = AprilTagging()
    localizer = Localizer(
        numOfRobotTags=2,
        tagOffset=np.array([0, 0]),
        distUnit=DistUnit.M,
        angleUnit=AngleUnit.DEG,
    )
    datalogger = Datalogger()
    capturer = PathCapturer("Experiment")

    # Utils
    pathCapturerRunning = False
    GRAPHICS_ENABLED = False
    np.set_printoptions(formatter={"float": lambda x: "{0:0.3f}".format(x)})
    fpss = []  # List of FPSs

    ##------------------------ Initialize Environment ------------------------##

    frame = cap.read()
    # Detect Corners on Raw Mat and Get Centers
    tagDetector.update(frame)
    fieldTagsCenters = tagDetector.getTagCentersByIds(localizer.fieldTagIds)

    # Calibrate Source
    viewportSide = frame.shape[0]
    cam_calibr = CameraCalibrator(
        fieldTagsCenters,
        frame_size=(viewportSide, viewportSide),
        padding=50,
        localizer=localizer,
    )
    reverted = cam_calibr.applyCalibrations(frame)

    ##-------------------------- Main Program/Loop ---------------------------##
    while cap.more():
        start_time = time.time()
        frame = cap.read()

        # If frame in not available skip this iteration
        if frame is None:
            continue

        # Calibrating Source
        calibrated = cam_calibr.applyCalibrations(frame)

        # Detecting Apriltags
        detectedMat = tagDetector.update(calibrated)

        # Update Tag Positions
        robotTagPositions = tagDetector.getTagCentersByIds(localizer.robotTagIds)

        # Calulate Poses, Velocities etc
        localizer.update(robotTagPositions)

        # Getters from Localizer Class
        robotPose = localizer.getRobotPose()
        robotVelocity = localizer.getRobotCurrentVelocity()

        print(f"Pose: {robotPose}, Velocity: {robotVelocity}")

        # Adding Step to Path Capturer
        capturer.update(robotPose)

        # Toggle Capturer State
        if keyboard.is_pressed("c"):
            if not capturer.captureEnabled:
                capturer.startCapturing()
        if keyboard.is_pressed("v"):
            if capturer.captureEnabled:
                capturer.stopCapturing()

        # Calculate FPS
        dt = time.time() - start_time + 0.000000000000000001
        fps = 1 / dt
        fpss.append(fps)

        # Preview FPS and Capturer State
        cv.putText(
            detectedMat,
            f"FPS: {fps:.0f} | Capturer State: {'Capturing' if capturer.captureEnabled else 'Not Capturing'}",
            (50, 50),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2,
            cv.LINE_AA,
        )

        # Graphics
        rawRobotPos = np.mean(np.array(robotTagPositions), axis=0).astype(int)

        if GRAPHICS_ENABLED:
            cv.line(
                detectedMat,
                rawRobotPos,
                (rawRobotPos[0], 0),
                (255, 0, 0),
                2,
            )
            cv.line(
                detectedMat,
                rawRobotPos,
                (viewportSide, rawRobotPos[1]),
                (255, 0, 0),
                2,
            )
            cv.line(
                detectedMat,
                rawRobotPos,
                (rawRobotPos[0], viewportSide),
                (255, 0, 0),
                2,
            )
            cv.line(
                detectedMat,
                rawRobotPos,
                (0, rawRobotPos[1]),
                (255, 0, 0),
                2,
            )

            cv.circle(detectedMat, tuple(rawRobotPos), 6, (0, 0, 255), -1)

        # Show Mats
        cv.imshow(
            "MultiView",
            np.concatenate(
                [
                    cv.resize(frame, (720, 720)),
                    cv.resize(detectedMat, (720, 720)),
                ],
                axis=1,
            ),
        )

        if cv.waitKey(1) & 0xFF == 27:
            break

##---------------------- Stop Capturing & Close Windows ----------------------##
cap.stop()
cv.destroyAllWindows()

##-------------------- Preview a Plot of the FPS Progress --------------------##
plt.title("FPS Representation")
samples = np.linspace(1, len(fpss), len(fpss))

print("Average FPS: ", np.mean(fpss))
plt.plot(samples, fpss, label="FPS")
plt.plot(samples, [np.mean(fpss)] * len(fpss), label="Average FPS")
plt.legend()

plt.xlabel("Sample No")
plt.ylabel("FPS")
plt.grid(True)
plt.show()
