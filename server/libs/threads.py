from copy import copy


def inference_handler(state, video, inference, stats):
    while state.run:
        state.current_frame = video.get_frame(inference, stats)
        state.new_frame = True


def io_handler(state, stats):
    previous_stats = copy(stats)
    while state.run:
        if (stats != previous_stats):
            print(stats) # emit message
            previous_stats = copy(stats)
