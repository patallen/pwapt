from __future__ import print_function

import sys
import mock
import unittest
from pwapt import middleware as mw
from pwapt.contrib import middleware as cmw

from tests.fake import FakeSamplerMiddleware, FakeHandlerMiddleware, make_fake_frames


def _expand_frames(frame):
    frames = []
    while frame:
        frames.insert(0, frame)
        frame = frame.f_back

    return frames


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


class TestContribMiddleware(unittest.TestCase):
    def setUp(self):
        mainframe = make_fake_frames(TEST_FRAME_INFOS)
        frames = _expand_frames(mainframe)

        class Callstack(object):
            def __init__(self):
                self.frames = frames

        callstack = Callstack()
        self.payload = {callstack: 10}

    @mock.patch('builtins.print')
    def test_dump_logging_middleware(self, mock_print):
        lmw = cmw.DumpLoggingMiddleware()
        res = lmw.process_payload(self.payload)
        size = sys.getsizeof(self.payload)
        mock_print.assert_called_with(
            'Dumped 10 samples in 1 unique groups. Size: {} bytes.'.format(size)
        )
        self.assertEqual(res, self.payload)

    def test_formatting_handler_middleware(self):
        fhmw = cmw.FormattingHandlerMiddleware()
        res = fhmw.process_payload(self.payload)

        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], tuple)
