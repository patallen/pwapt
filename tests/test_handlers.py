import copy
import unittest
from mock import make_fake_frames

from pwapt.handlers import FlameGraphSampleHandler


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


class TestFlameGraphSampleHandler(unittest.TestCase):
    def setUp(self):
        self.frames = []
        self.handler = FlameGraphSampleHandler()
        for inf in (
            TEST_FRAME_INFO1, copy.copy(TEST_FRAME_INFO1), TEST_FRAME_INFO2
        ):
            self.frames.append(make_fake_frames(inf))

    def test_handle(self):
        self.handler.handle(self.frames[0])
        stack_string = "sillyboy`get_silly;seltzer`sparkle"
        dump = self.handler.dump()

        self.assertEqual(dump.keys()[0], stack_string)
        self.assertEqual(sum(dump.values()), 1)

    def test_sample_count(self):
        for frame in self.frames:
            self.handler.handle(frame)

        self.assertEqual(self.handler.sample_count, 3)

    def test_reset(self):
        for frame in self.frames:
            self.handler.handle(frame)

        self.handler.reset()
        self.assertEqual(self.handler.sample_count, 0)

    def test_dump(self):
        for frame in self.frames:
            self.handler.handle(frame)

        dump = self.handler.dump()
        self.assertEqual(len(dump.keys()), 2)


if __name__ == '__main__':
    unittest.main()
