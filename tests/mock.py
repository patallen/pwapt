

class FakeCode(object):
    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class FakeFrame(object):
    def __init__(self, f_code, f_globals, previous):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_back = previous


EXAMPLE_FRAME_INFOS = [
    {
        "f_code": {
            "co_filename": "/you/are/such/a/sillyboy.py",
            "co_name": "get_silly"
        },
        "f_globals": {
            "__name__": "sillyboy"
        }
    },
    {
        "f_code": {
            "co_name": "sparkle",
            "co_filename": "/i/love/seltzer.py"
        },
        "f_globals": {
            "__name__": "seltzer"
        }
    },
    {
        "f_code": {
            "co_name": "win",
            "co_filename": "/breakfast/of/champions.py"
        },
        "f_globals": {
            "__name__": "champions"
        }
    }
]


def make_fake_code(code_info):
    return FakeCode(
        co_filename=code_info.get('co_filename'),
        co_name=code_info.get('co_name')
    )


def make_fake_frame(frame_info, previous_frame=None):
    """Build a FakeFrame.

    :param frame_info: <dict> Containing info on f_code and f_globals.
    :param previous_frame: <FakeFrame> 
    :returns: <FakeFrame> The highest-level FakeFrame in the callstack.
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


