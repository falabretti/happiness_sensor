class State:
    def __init__(self):
        self.run = True
        self.current_frame = None
        self.new_frame = False


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
