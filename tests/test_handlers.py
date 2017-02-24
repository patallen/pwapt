import copy
import unittest
from fake import make_fake_frames

from pwapt import callstack as cs
from pwapt import handlers as hlr


TEST_FRAME_INFO1 = [
    {
        "f_code": {"co_name": "get_silly"},
        "f_globals": {"__name__": "sillyboy"}
    },
    {
        "f_code": {"co_name": "sparkle"},
        "f_globals": {"__name__": "seltzer"}
    },
]

TEST_FRAME_INFO2 = [
    {
        "f_code": {"co_name": "get_silly"},
        "f_globals": {"__name__": "sillyboy"}
    },
    {
        "f_code": {"co_name": "sparkle"},
        "f_globals": {"__name__": "seltzer"}
    },
    {
        "f_code": {"co_name": "lucky_charms"},
        "f_globals": {"__name__": "cereal"}
    }
]

config = {
    'SAMPLING_INTERVAL': .0005,
    'HANDLER_DUMP_INTERVAL': 30,
}


class TestSampleHandler(unittest.TestCase):
    def setUp(self):
        self.frames = []
        self.handler = hlr.SampleHandler(config)
        for inf in (
            TEST_FRAME_INFO1,
            copy.copy(TEST_FRAME_INFO1),
            TEST_FRAME_INFO2
        ):
            frames = make_fake_frames(inf)
            self.frames.append(frames)

    def test_handle(self):
        callstack = cs.CallStack.from_frame(self.frames[-1])

        self.handler.handle(self.frames[-1])

        self.assertIn(callstack, self.handler)
        self.assertEqual(str(callstack), str(self.handler.store.keys()[0]))

    def test_sample_count(self):
        frames = (f for f in self.frames)

        self.handler.handle(next(frames))
        self.assertEqual(self.handler.sample_count, 1)

        self.handler.handle(next(frames))
        self.assertEqual(self.handler.sample_count, 2)

        self.handler.handle(next(frames))
        self.assertEqual(self.handler.sample_count, 3)

    def test_reset(self):
        for f in self.frames:
            self.handler.handle(f)

        self.assertEqual(self.handler.sample_count, 3)
        self.handler.reset()
        self.assertEqual(self.handler.sample_count, 0)

    def test_dump(self):
        for f in self.frames:
            self.handler.handle(f)

        a = cs.CallStack.from_frame(self.frames[2])
        b = cs.CallStack.from_frame(self.frames[0])

        dump = self.handler.dump()
        self.assertEqual(dump[a], 1)
        self.assertEqual(dump[b], 2)

    def test_contains(self):
        control = cs.CallStack.from_frame(self.frames[2])
        for f in self.frames:
            self.handler.handle(f)

        self.assertIn(control, self.handler)

if __name__ == '__main__':
    unittest.main()
