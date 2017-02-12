import time
from abc import ABCMeta, abstractmethod


class BaseStack(ABCMeta):
    formatter_class = None

    def __init__(self, frame):
        self.ts = time.time()
        self._top_frame = frame

    @abstractmethod
    def final_format(self):
        pass
    
    @property
    def formatted(self):
        pass


    @property
    def formatted_frames(self):
        frames = []
        for frame in self.frames:
            frames.append(self.formatter_class.format_frame(frame))
        return frames

    @property
    def frames(self):
        rv = []
        frame = self._top_frame
        while frame is not None:
            rv.append(frame)
            frame = frame.f_back
        return rv

    def __repr__(self):
        return self.formatted()

    def __str__(self):
        return self.formatted()

    def __eq__(self, other):
        return self.formatted() == other.formatted()


class FrameFormatter(ABCMeta):

    @abstractmethod
    def format_frame(self, frame):
        pass


class FlameGraphFrameFormatter(FrameFormatter):
    @staticmethod
    def format_frame(frame):
        name = frame.f_code.co_name
        filename = frame.f_globals.get('__name__')
        return "%s`%s;" % (name, filename)
 

class FlameGraphCallStack(BaseStack):
    formatter_class = FlameGraphFrameFormatter

    def formatted(self):
        return ";".join(self.formatted_frames)
