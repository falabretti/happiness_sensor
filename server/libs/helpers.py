import cv2 as cv
import numpy as np


def prepare_frame(frame, input_shape):
    b, c, h, w = input_shape

    input_frame = cv.resize(frame, (w, h))
    input_frame = input_frame.transpose((2, 0, 1))
    input_frame = input_frame.reshape((b, c, h, w))

    return input_frame


def draw_boxes(frame, faces, color=(0, 255, 0)):
    h, w = frame.shape[:2]

    for face in faces:
        box = face[3:7] * np.array([w, h, w, h])
        xmin, ymin, xmax, ymax = box.astype("int")

        cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness=1)

    return frame
