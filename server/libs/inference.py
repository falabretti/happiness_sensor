import cv2 as cv

from openvino.inference_engine import IENetwork, IEPlugin

from .helpers import prepare_frame


class Inference:
    def __init__(self, settings):
        cpu_extension = settings.cpu_extension
        self.plugin = IEPlugin(device=settings.device)
        self.face_detection = FaceDetection(settings.face_detection_xml,
                                            self.plugin, cpu_extension=cpu_extension, device=settings.device)
        self.emotion_recognition = EmotionRecognition(settings.emotion_recognition_xml,
                                                      self.plugin, cpu_extension=cpu_extension, device=settings.device)


class Network:
    def __init__(self, model, plugin, device='CPU', cpu_extension=None, num_requests=2):
        self.net = None
        self.input_layer = None
        self.output_layer = None
        self.exec_net = None
        self.cur_req_id = 0
        self.next_req_id = 1

        self._load_model(model, plugin, device, cpu_extension, num_requests)

    def _load_model(self, model, plugin, device, cpu_extension, num_requests):
        xml_path = model
        bin_path = model.split('.')[0] + '.bin'

        self.net = IENetwork(model=xml_path, weights=bin_path)
        self.input_layer = next(iter(self.net.inputs))
        self.output_layer = next(iter(self.net.outputs))

        if cpu_extension and device == 'CPU':
            plugin.add_cpu_extension(cpu_extension)

        self.exec_net = plugin.load(
            network=self.net, num_requests=num_requests)

    def _infer_req(self, frame, request_id):
        self.exec_net.start_async(request_id=request_id, inputs={
                                  self.input_layer: frame})

    def get_input_shape(self):
        return self.net.inputs[self.input_layer].shape

    def _swap_requests(self):
        self.cur_req_id, self.next_req_id = self.next_req_id, self.cur_req_id

    def _wait(self, request_id):
        return self.exec_net.requests[request_id].wait(-1)


class FaceDetection(Network):
    def __init__(self, model, plugin, device='CPU', cpu_extension=None):
        super().__init__(model, plugin, device, cpu_extension, num_requests=3)
        self.is_first_frame = True

    def infer(self, next_frame):
        input_frame = prepare_frame(next_frame, self.get_input_shape())

        self._infer_req(input_frame, self.next_req_id)

        if self.is_first_frame:
            self.is_first_frame = False
            self._swap_requests()
            return []

        faces = self.get_results(self.cur_req_id)

        return faces

    def get_results(self, request_id):
        faces = None

        if self._wait(request_id) == 0:
            results = self.exec_net.requests[request_id].outputs[self.output_layer]
            faces = [x for x in results[0][0] if x[2] > 0.8]

        self._swap_requests()
        return faces


class EmotionRecognition(Network):

    def __init__(self, model, plugin, device='CPU', cpu_extension=None):
        super().__init__(model, plugin, device, cpu_extension)

    def infer(self, faces):
        results = []

        for idx in range(len(faces) + 1):
            if idx == len(faces):
                result = self._get_results(self.cur_req_id)
                results.append(result)
                break

            face_frame = faces[idx]
            try:
                input_face = prepare_frame(face_frame, self.get_input_shape())
            except cv.error:
                if len(faces) == 1:
                    return []
                continue

            self._infer_req(input_face, self.next_req_id)

            if idx == 0:
                self._swap_requests()
                continue

            result = self._get_results(self.cur_req_id)
            results.append(result)

        return results

    def _get_results(self, request_id):
        if self._wait(request_id) == 0:
            result = self.exec_net.requests[request_id].outputs[self.output_layer]
            self._swap_requests()
            return result
