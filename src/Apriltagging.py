import cv2 as cv
from pupil_apriltags import Detector

PLOT_APRIL_TAGS = False


class AprilTagging:
    tagsDetected = []
    detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0,
    )

    def update(self, frame):
        output = frame
        grayscaleImage = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
        self.tagsDetected = self.detector.detect(grayscaleImage)

        if PLOT_APRIL_TAGS:
            output = output.copy()
            for tag in self.tagsDetected:
                ptA, ptB, ptC, ptD = tag.corners

                ptB = (int(ptB[0]), int(ptB[1]))
                ptC = (int(ptC[0]), int(ptC[1]))
                ptD = (int(ptD[0]), int(ptD[1]))
                ptA = (int(ptA[0]), int(ptA[1]))

                cv.line(output, ptA, ptB, (255, 0, 0), 2)
                cv.line(output, ptB, ptC, (255, 0, 0), 2)
                cv.line(output, ptC, ptD, (255, 0, 0), 2)
                cv.line(output, ptD, ptA, (255, 0, 0), 2)

                cv.putText(
                    output,
                    str(tag.tag_id),
                    (ptB[0] + 10, ptB[1] + 15),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                    cv.LINE_AA,
                )

        return output

    def getTagCenterById(self, id):
        filteredArr = list(filter(lambda x: x.tag_id == id, self.tagsDetected))
        return filteredArr[0].center if filteredArr else None

    def getTagCentersByIds(self, ids):
        detectedTags = list(
            filter(lambda x: x.tag_id in set(ids), self.tagsDetected)
        )
        centers = [tag.center for tag in detectedTags]
        while len(centers) < 2:
            centers.append([0, 0])

        return centers[:2]
