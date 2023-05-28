import cv2 as cv
import threading
from collections import deque


class WebcamStreaming(threading.Thread):
    def __init__(self, queue_size=10):
        super().__init__()
        self.queue_size = queue_size
        self.frame_queue = deque(maxlen=queue_size)
        self.running = False

    def run(self, src=0):
        self.running = True
        capture = cv.VideoCapture(src)

        while self.running:
            ret, frame = capture.read()
            if not ret:
                break

            if len(self.frame_queue) >= self.queue_size:
                self.frame_queue.popleft()
            self.frame_queue.append(frame)

        capture.release()

    def stop(self):
        self.running = False

    def read(self):
        if len(self.frame_queue) > 0:
            return self.frame_queue[-1]
        return None

    def isQEmpty(self):
        return self.running
