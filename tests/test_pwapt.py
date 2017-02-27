import unittest

import mock
from mock import MagicMock

from pwapt import Pwapt
from pwapt.config import Config
from pwapt.sampler import Sampler
from pwapt.handlers import SampleHandler
from pwapt.exceptions import PwaptConfigException
import gevent.monkey


class MockHandler(object):
    pass


class MockSampler(object):
    def __init__(self):
        self.start = mock.MagicMock(return_value=None)


class TestPwaptApplication(unittest.TestCase):
    def setUp(self):
        self.pwapt = Pwapt()
        self.pwapt.config.from_dict({
            'SAMPLING_INTERVAL': 10,
            'HANDLER_DUMP_INTERVAL': 30
        })

    def test_initialization(self):
        self.assertNotEqual(self.pwapt.config, None)
        self.assertFalse(self.pwapt._started)
        self.assertEqual(self.pwapt.sampler, None)
        self.assertEqual(self.pwapt.handler, None)

    def test_exceptions(self):
        missing = PwaptConfigException.MISSING_REQUIRED
        missingc = PwaptConfigException.MISSING_CONFIG

        self.pwapt.config = Config()
        with self.assertRaisesRegexp(PwaptConfigException, missingc):
            self.pwapt.run()

        self.pwapt.config.from_dict({"HELLO": 'zzz'})
        with self.assertRaisesRegexp(PwaptConfigException, missing):
            self.pwapt.run()

    def test_get_sampler_classes(self):
        handler = self.pwapt._make_handler()
        sampler = self.pwapt._make_sampler(handler)
        self.assertIsInstance(sampler, Sampler)
        self.assertIsInstance(handler, SampleHandler)

    def test_run_calls(self):
        self.pwapt._make_handler = MagicMock(
            return_value=SampleHandler(self.pwapt.config)
        )
        self.pwapt._make_sampler = MagicMock(return_value=Sampler(
            self.pwapt.handler, self.pwapt.config)
        )

        with mock.patch('time.time', return_value=1):
            self.pwapt.run()
        self.assertEqual(self.pwapt._started, 1)

        assert self.pwapt._make_handler.called
        assert self.pwapt._make_sampler.called

        self.assertIsInstance(self.pwapt.sampler, Sampler)
        self.assertIsInstance(self.pwapt.handler, SampleHandler)

    @mock.patch('gevent.spawn', lambda method, *a, **kw: method(*a, **kw))
    def test_sampler_start(self):
        sampler = MockSampler()
        self.pwapt._make_sampler = lambda x: sampler
        self.pwapt.run()
        assert sampler.start.called
