from flask import Flask, Response
from threading import Thread

import cv2 as cv

from libs.video import VideoInput
from libs.data import State
from libs.threads import inference_handler

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

if __name__ == '__main__':
    state = State()
    video = VideoInput()

    inference_thread = Thread(target=inference_handler, args=[state, video])
    
    inference_thread.start()
    app.run(host='0.0.0.0', threaded=True, debug=False)
    inference_thread.join()