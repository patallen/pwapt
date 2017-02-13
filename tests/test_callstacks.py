import unittest
from mock import make_fake_frames

from pyfiler.callstack import FlameGraphCallStack


TEST_FRAME_INFOS = [
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


class TestFlameGraphCallStack(unittest.TestCase):
    def setUp(self):
        self.frame_infos = TEST_FRAME_INFOS
        self.top_frame = make_fake_frames(self.frame_infos)
        self.callstack = FlameGraphCallStack(self.top_frame)

    def test_expansion_of_top_frame_to_frames(self):
        self.assertEqual(len(self.callstack.frames), len(self.frame_infos))

    def test_formatted_stack(self):
        final = "sillyboy`get_silly;seltzer`sparkle;champions`win"
        self.assertEqual(final, str(self.callstack.formatted))


if __name__ == '__main__':
    unittest.main()
