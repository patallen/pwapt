import unittest

import mock
from mock import MagicMock

from pwapt import Pwapt
from pwapt.sampler import Sampler
from pwapt.handlers import SampleHandler
from pwapt.exceptions import PwaptConfigException


class MockHandler(object):
    pass


class MockSampler(object):
    pass


class TestPwaptApplication(unittest.TestCase):
    def setUp(self):
        self.pwapt = Pwapt()

    def test_initialization(self):
        self.assertNotEqual(self.pwapt.config, None)
        self.assertFalse(self.pwapt._started)
        self.assertEqual(self.pwapt.sampler, None)
        self.assertEqual(self.pwapt.handler, None)

    def test_exceptions(self):
        missing = PwaptConfigException.MISSING_REQUIRED
        missingc = PwaptConfigException.MISSING_CONFIG
        with self.assertRaisesRegexp(PwaptConfigException, missingc):
            self.pwapt.run()

        self.pwapt.config.from_dict({"HELLO": 'zzz'})
        with self.assertRaisesRegexp(PwaptConfigException, missing):
            self.pwapt.run()

    def test_get_handler_class(self):
        self.assertEqual(self.pwapt._get_handler_class(), SampleHandler)

    def test_get_sampler_class(self):
        self.assertEqual(self.pwapt._get_sampler_class(), Sampler)

    def test_get_sampler_classes(self):
        sampler_class = self.pwapt._get_sampler_class()
        handler_class = self.pwapt._get_handler_class()
        self.assertEqual(sampler_class, Sampler)
        self.assertEqual(handler_class, SampleHandler)

    def test_run_calls(self):
        self.pwapt.config.from_dict({
            'SAMPLING_INTERVAL': 10,
            'HANDLER_DUMP_INTERVAL': 30
        })
        self.pwapt._get_sampler_class = MagicMock(return_value=Sampler)
        self.pwapt._get_handler_class = MagicMock(return_value=SampleHandler)

        with mock.patch('time.time', return_value=1):
            self.pwapt.run()
        self.assertEqual(self.pwapt._started, 1)

        assert self.pwapt._get_handler_class.called
        assert self.pwapt._get_sampler_class.called
