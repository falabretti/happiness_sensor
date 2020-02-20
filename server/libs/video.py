import cv2 as cv

class VideoInput:
    def __init__(self):
        self._input_stream = 0
        self._video = cv.VideoCapture(self._input_stream)
        _, self.frame = self._video.read()

    def get_frame(self):
        has_frame, next_frame = self._video.read()
        if not has_frame: return

        return next_frame