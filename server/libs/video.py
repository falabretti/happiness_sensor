import cv2 as cv

from .helpers import draw_boxes, get_face_frames, get_boxes


class VideoInput:
    def __init__(self, settings):
        self._input_stream = settings.input_stream
        self._video = cv.VideoCapture(self._input_stream)
        self.flip_code = settings.flip_code

        self._video.set(cv.CAP_PROP_FRAME_WIDTH, settings.frame_width)
        self._video.set(cv.CAP_PROP_FRAME_HEIGHT, settings.frame_height)

        _, self.frame = self._video.read()

    def get_frame(self, inference, stats):
        has_frame, next_frame = self._video.read()
        if not has_frame:
            return self.frame

        faces = inference.face_detection.infer(next_frame)
        boxes = get_boxes(next_frame, faces)
        face_frames = get_face_frames(boxes, next_frame)
        emotions = inference.emotion_recognition.infer(face_frames)

        if (len(faces) > 0):
            self.frame = draw_boxes(next_frame, boxes, emotions)

        aux_frame = self.frame.copy()
        self.frame = next_frame

        stats.update(boxes, emotions)

        if self.flip_code is not None:
            aux_frame = cv.flip(aux_frame, self.flip_code)

        return aux_frame
