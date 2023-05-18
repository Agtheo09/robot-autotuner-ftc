from threading import Thread
from queue import Queue
import cv2 as cv


class WebcamStreaming:
    def __init__(self, src=0, qMaxLength=129):
        self.frameQ = Queue(maxsize=qMaxLength)
        # self.frameQ = []
        self.stream = cv.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.frameQ.put(self.frame)

        self.stopped = False

    def start(self):
        self.thread = Thread(target=self.update, args=())
        self.thread.start()

        return self

    def update(self):
        while True:
            if self.stopped:
                return

            print(self.frameQ.qsize())

            if not self.frameQ.full():
                (self.grabbed, self.frame) = self.stream.read()

                if not self.grabbed:
                    self.stop()
                    return

                self.frameQ.put(self.frame)
                # print(self.frameQ.qsize())

    def read(self):
        return self.frameQ.get()

    def stop(self):
        self.stopped = True

    def isQEmpty(self):
        return self.frameQ.qsize > 0
