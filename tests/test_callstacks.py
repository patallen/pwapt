import unittest
from fake import make_fake_frames

from pwapt import callstack as cs


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


class BaseCallStackTestCase(unittest.TestCase):
    def setUp(self):
        self.frame_infos = TEST_FRAME_INFOS
        self.top_frame = make_fake_frames(self.frame_infos)


class TestCallStack(BaseCallStackTestCase):
    def test_from_frame(self):
        callstack = cs.CallStack.from_frame(self.top_frame)
        self.assertEqual(3, len(callstack.frames))

    def test_callstack_depth(self):
        callstack = cs.CallStack.from_frame(self.top_frame)
        self.assertEqual(callstack.depth, 3)

    def test_callstack_hash(self):
        callstack = cs.CallStack.from_frame(self.top_frame)
        fns = ('/you/are/such/a/sillyboy.py/i/love/'
               'seltzer.py/breakfast/of/champions.py')
        self.assertEqual(hash(callstack), hash(fns))



if __name__ == '__main__':
    unittest.main()
