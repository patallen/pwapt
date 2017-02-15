import unittest

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
