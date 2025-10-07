from collections import deque

class VideoBuffer:
    def __init__(self, maxlength=450):
        self.buffer = deque(maxlen=maxlength)

    def add_frame(self, frame):
        self.buffer.append(frame)

    def get_buffer(self):
        return list(self.buffer)