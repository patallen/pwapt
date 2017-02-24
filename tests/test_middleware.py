import unittest
from pwapt import middleware as mw
from tests.fake import FakeSamplerMiddleware, FakeHandlerMiddleware
from pwapt.exceptions import PwaptConfigException


class TestMiddlewareManagers(unittest.TestCase):
    def setUp(self):
        self.app_home = '../'
        self.config = {
            'SAMPLER_MIDDLEWARE_CLASSES': [
                'tests.fake.FakeSamplerMiddleware'
            ],
            'HANDLER_MIDDLEWARE_CLASSES': [
                'tests.fake.FakeHandlerMiddleware'
            ]
        }

        self.empty_config = {}

    def test_load_middleware_from_config(self):
        mw.MiddlewareManager.CONFIG_NAME = 'SAMPLER_MIDDLEWARE_CLASSES'

        with self.assertRaises(TypeError):
            mw.MiddlewareManager.from_config(self.config)

        mw.MiddlewareManager.METHOD_STRING = 'nope'
        with self.assertRaises(AttributeError):
            mw.MiddlewareManager.from_config(self.config)

    def test_sampler_middleware_manager(self):
        mwm = mw.SamplerMiddlewareManager.from_config(self.config)
        self.assertIn(FakeSamplerMiddleware, mwm.middleware_classes)

        rv = mwm.process_sample({})
        self.assertEqual(rv, 'GET_TESTED')

    def test_handler_middleware_manager(self):
        mwm = mw.HandlerMiddlewareManager.from_config(self.config)
        self.assertIn(FakeHandlerMiddleware, mwm.middleware_classes)

        rv = mwm.process_payload({})
        self.assertEqual(rv, 'PAYLOADED')
