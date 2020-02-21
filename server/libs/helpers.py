import cv2 as cv
import numpy as np


def prepare_frame(frame, input_shape):
    b, c, h, w = input_shape

    input_frame = cv.resize(frame, (w, h))
    input_frame = input_frame.transpose((2, 0, 1))
    input_frame = input_frame.reshape((b, c, h, w))

    return input_frame


def draw_boxes(frame, boxes, emotions):
    h, w = frame.shape[:2]
    emotion_list = ['neutral', 'happy', 'sad', 'surprise', 'anger']

    for box, emotion in zip(boxes, emotions):
        color = (0, 255, 0) if emotion.argmax() == 1 else (0, 0, 255)
        xmin, ymin, xmax, ymax = box
        cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness=2)

    return frame

def get_boxes(frame, detections):
    h, w = frame.shape[:2]
    boxes = []

    for detection in detections:
        box = detection[3:7] * np.array([w, h, w, h])
        xmin, ymin, xmax, ymax = box.astype('int')
        boxes.append((xmin, ymin, xmax, ymax))

    return boxes

def get_face_frames(boxes, frame):
    h, w = frame.shape[:2]
    face_frames = []

    for box in boxes: 
        xmin, ymin, xmax, ymax = box
        face_frame = frame[ymin:ymax, xmin:xmax]
        face_frames.append(face_frame)

    return face_frames
