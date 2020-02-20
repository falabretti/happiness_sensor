def inference_handler(state, video, inference):
    while state.run:
        state.current_frame = video.get_frame(inference)
        state.new_frame = True
