import cv2 as cv

from openvino.inference_engine import IENetwork, IEPlugin

from .helpers import prepare_frame

class Inference:
    def __init__(self):
        self.plugin = IEPlugin(device='CPU')
        self.face_detection = FaceDetection(r'extension\models\face-detection-retail-0005\FP16\face-detection-retail-0005.xml',
                                            self.plugin,
                                            device='CPU',
                                            cpu_extension=r"C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\inference_engine\bin\intel64\Release\cpu_extension_avx2.dll")


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
        self.AUX_REQ_ID = 2
        self.is_first_frame = True

    def infer(self, next_frame):
        input_frame = prepare_frame(next_frame, self.get_input_shape())

        self._infer_req(input_frame, self.next_req_id)

        if self.is_first_frame:
            self.is_first_frame = False
            self._swap_requests()
            return []

        faces = self.get_results(self.cur_req_id)
        # frame = draw_boxes(next_frame, faces)

        return faces

    def get_results(self, request_id):
        faces = None

        if self._wait(request_id) == 0:
            results = self.exec_net.requests[request_id].outputs[self.output_layer]
            faces = [x for x in results[0][0] if x[2] > 0.8]

        if request_id != 2:
            self._swap_requests()

        return faces