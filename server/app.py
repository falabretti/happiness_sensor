from flask import Flask, Response
from flask_socketio import SocketIO
from threading import Thread
from flask_cors import CORS

import cv2 as cv
import signal

from libs.video import VideoInput
from libs.data import State, Stats, Settings
from libs.threads import inference_handler, io_handler
from libs.inference import Inference
from libs.helpers import get_log_filename

import logging

logging.basicConfig(level=logging.INFO, filename=get_log_filename(),
                    format='%(levelname)s - %(asctime)s - %(name)s:%(lineno)d - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

logging.getLogger('engineio.server').setLevel(logging.ERROR)
logging.getLogger('socketio.server').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return 'Go to /video_feed to see the video'


@app.route('/video_feed')
def video_feed():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


def stream():
    while True:
        if state.new_frame:
            _, encoded_frame = cv.imencode('.jpg', state.current_frame)
            string_data = encoded_frame.tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: text/plain\r\n\r\n'+string_data+b'\r\n')
            state.new_frame = False


def stop_run(signum, frame):
    state.run = False
    raise KeyboardInterrupt


if __name__ == '__main__':
    signal.signal(signal.SIGINT, stop_run)

    state = State()
    settings = Settings()
    video = VideoInput(settings)
    inference = Inference(settings)
    stats = Stats()

    inference_thread = Thread(target=inference_handler, args=[
                              state, video, inference, stats])
    io_thread = Thread(target=io_handler, args=[state, stats, socketio])

    inference_thread.start()
    io_thread.start()

    socketio.run(app, host='0.0.0.0', debug=False)

    inference_thread.join()
    io_thread.join()
