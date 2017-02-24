import unittest
import mock
from mock import MagicMock

from pwapt.handlers import SampleHandler
from pwapt.app import Pwapt
from pwapt.sampler import Sampler

from fake import make_fake_frames


config = {
    'SAMPLING_INTERVAL': .01,
    'HANDLER_DUMP_INTERVAL': 10,
}


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

class SamplerTestCase(unittest.TestCase):
    def setUp(self):
        self.pwapt = Pwapt()
        self.handler = SampleHandler(config)
        self.sampler = Sampler(self.handler, config)

    def test_sampler_init(self):
        self.assertIsNotNone(self.sampler.handler)
        self.assertEqual(self.sampler.interval, .01)

    def test_sampler_start(self):
        with mock.patch('time.time', return_value=1000):
            self.sampler.start()
            self.assertEqual(self.sampler._started_at, 1000)

    def test_sampler_delete(self):
        timer = self.sampler._started_at
        del self.sampler
        self.assertIsNone(timer)

    def test_sampler_reset(self):
        with mock.patch('time.time', return_value=1000):
            self.sampler.reset()
            self.assertEqual(self.sampler._last_reset, 1000)

    def test_sampler_stop(self):
        with mock.patch('time.time', return_value=1000):
            self.sampler.stop()
            self.assertEqual(self.sampler._last_reset, 1000)
            self.assertIsNone(self.sampler._started_at)

    def test_sampler_session_duration(self):
        self.sampler._last_reset = 0

        with mock.patch('time.time', return_value=1000):
            self.assertEqual(self.sampler.session_duration, 1000)

        self.sampler._last_reset = None
        with mock.patch('time.time', return_value=1000):
            self.assertEqual(self.sampler.session_duration, 0)

    def test_sampler_total_duration(self):
        self.sampler._started_at = 0

        with mock.patch('time.time', return_value=1000):
            self.assertEqual(self.sampler.total_duration, 1000)

        self.sampler._started_at = None
        self.assertEqual(self.sampler.total_duration, 0)

    def test_middleware_called_with(self):
        self.frame = make_fake_frames(TEST_FRAME_INFOS)
        self.sampler.middleware.process_sample = MagicMock(
            return_value=self.frame
        )
        self.sampler._sample(1, self.frame)

        assert self.sampler.middleware.process_sample.called

