from flask import Flask, Response
from threading import Thread

import cv2 as cv
import signal

from libs.video import VideoInput
from libs.data import State
from libs.threads import inference_handler
from libs.inference import Inference

app = Flask(__name__)


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
    video = VideoInput()
    inference = Inference()

    inference_thread = Thread(target=inference_handler, args=[state, video, inference])

    inference_thread.start()
    app.run(host='0.0.0.0', threaded=True, debug=False)
    inference_thread.join()
