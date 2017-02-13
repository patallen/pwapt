
class FakeCode(object):
    """Mock for the python core's Code object.

    Used to store information on the underlying code of a Frame.
    """

    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class FakeFrame(object):
    """Mock for python core's Frame object.

    Holds information on the current stack frame. We can easily
    back into an entire call stack by looping on Frame.f_back.
    """

    def __init__(self, f_code, f_globals, previous):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_back = previous


def make_fake_code(code_info):
    """Build a FakeCode.

    :param code_info: <dict> Contains:
        - co_name (name of the calling function)
        - co_filename (name of the module in which the function resides)
    """
    return FakeCode(
        co_filename=code_info.get('co_filename'),
        co_name=code_info.get('co_name')
    )


def make_fake_frame(frame_info, previous_frame=None):
    """Build a FakeFrame.

    :param frame_info: <dict> Contains:
        - f_code (FakeCode object)
        - f_globals (dict of all globals captured)
    :param previous_frame: <FakeFrame>
    :returns: <FakeFrame>
    """
    code_info = frame_info.get('f_code')
    globs = frame_info.get('f_globals')
    code = make_fake_code(code_info)
    return FakeFrame(code, globs, previous_frame)


def make_fake_frames(frame_infos):
    """Build a set of FakeFrames.

    :param frame_infos: <list of dicts> Info for each frame's code/globals
    :returns: <FakeFrame> The highest-level FakeFrame in the callstack.
    """
    frame = None
    previous = None
    for frame_inf in frame_infos:
        frame = make_fake_frame(frame_inf, previous_frame=previous)
        previous = frame
    return frame
