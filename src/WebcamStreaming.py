from threading import Thread
from queue import Queue
import cv2 as cv
import threading


class WebcamStreaming:
    def __init__(self, src=0, qMaxLength=120):
        self.stream = cv.VideoCapture(src)
        self.frameQ = Queue(maxsize=qMaxLength)

        self.stopped = False
        self.queueLock = threading.Lock()

    def start(self):
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        return self

    def update(self):
        while True:
            if self.stopped:
                return

            if not self.frameQ.full():
                (self.grabbed, self.frame) = self.stream.read()

                if not self.grabbed:
                    self.stop()
                    return

                with self.queueLock:
                    self.frameQ.put(self.frame)

    def read(self):
        return self.frameQ.get()

    def stop(self):
        self.stopped = True
        self.thread.join()

    def isQEmpty(self):
        return self.frameQ.qsize() > 0
