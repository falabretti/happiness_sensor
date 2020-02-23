from copy import copy
import json
import logging

log = logging.getLogger(__name__)

def inference_handler(state, video, inference, stats):
    while state.run:
        state.current_frame = video.get_frame(inference, stats)
        state.new_frame = True


def io_handler(state, stats, socketio):
    previous_stats = copy(stats)
    while state.run:
        if (stats != previous_stats):
            log.info('NEW STATS: %s', json.dumps(stats.__dict__))
            socketio.emit('stats', json.dumps(stats.__dict__))
            previous_stats = copy(stats)
