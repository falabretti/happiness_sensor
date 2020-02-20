def inference_handler(state, video):
    while state.run:
        state.current_frame = video.get_frame()
        state.new_frame = True