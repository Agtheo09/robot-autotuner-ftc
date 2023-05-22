import cv2 as cv
import queue
import threading
from cvzone import FPS

fpsReader = FPS()
minFPS = 200
maxFPS = 0


# Function to read frames from the webcam and put them in a queue
def capture_frames(queue):
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        queue.put(frame)

    cap.release()


# Function to process frames from the queue
def process_frames(queue):
    while True:
        frame = queue.get()

        # Perform your processing tasks on the frame here
        # Example: Convert frame to grayscale
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        fps, plusFPS = fpsReader.update(
            gray_frame, pos=(50, 80), color=(0, 255, 0), scale=5, thickness=5
        )

        # Display the processed frame
        cv.imshow("Processed Frame", plusFPS)
        if cv.waitKey(1) == ord("q"):
            break

    cv.destroyAllWindows()


# Create a queue to store the frames
frame_queue = queue.Queue(
    maxsize=5
)  # Adjust the maxsize as per your requirements

# Create and start the thread for capturing frames
capture_thread = threading.Thread(target=capture_frames, args=(frame_queue,))
capture_thread.start()

# Start processing the frames
process_frames(frame_queue)
