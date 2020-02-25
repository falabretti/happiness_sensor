import os
from configparser import ConfigParser
from shutil import copyfile


class State:
    def __init__(self):
        self.run = True
        self.current_frame = None
        self.new_frame = False


class Settings:
    def __init__(self):
        self.config = ConfigParser()
        if not os.path.isfile('./config.ini'):
            copyfile('./config.ini.default', './config.ini')

        self.config.read('./config.ini')
        self._get_config()

    def _get_config(self):
        input_stream = self.config.get('main', 'input_stream')
        self.input_stream = int(
            input_stream) if input_stream.isnumeric() else input_stream

        self.cpu_extension = self.config.get('main', 'cpu_extension')
        self.face_detection_xml = self.config.get('main', 'face_detection_xml')
        self.emotion_recognition_xml = self.config.get(
            'main', 'emotion_recognition_xml')
        self.device = self.config.get('main', 'device')

        flip_code = self.config.get('main', 'flip_code')
        self.flip_code = None if flip_code == 'None' else int(flip_code)

        resolution = self.config.get('main', 'resolution')
        w, h = resolution.replace(' ', '').split('x')
        self.frame_width = int(w)
        self.frame_height = int(h)


class Stats:
    def __init__(self):
        self.faces = 0
        self.happy = 0
        self.sad = 0
        self.ratio = 0

    def __str__(self):
        return f'faces: {self.faces}, happy: {self.happy}, sad: {self.sad}, ratio: {self.ratio}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def update(self, boxes, emotions):
        self.faces = len(boxes)

        self.happy = 0
        for emotion in emotions:
            if emotion is not None:
                self.happy += 1 if emotion.argmax() == 1 else 0

        self.sad = self.faces - self.happy if self.happy is not None else 0
        self.ratio = self.happy / self.faces if self.faces != 0 else 0.5
