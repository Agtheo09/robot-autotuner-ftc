from threading import Thread, Lock
from queue import Queue
import cv2 as cv
import time


class VideoStream:
    # * @param path: path to the video file or index of video source(camera 0 by default)
    # * @param queueSize: max queue size
    def __init__(self, path=0, queueSize=20):
        self.stream = cv.VideoCapture(path)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        self.t = Thread(target=self.update, args=())

        self.t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            if self.Q.full():
                # Wait for a short period of time to allow frames to be consumed
                time.sleep(0.01)
                continue
            (grabbed, frame) = self.stream.read()
            if not grabbed:
                self.stop()
                return
            self.Q.put(frame)

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() >= 1

    def stop(self):
        self.stopped = True
        self.t.join()
