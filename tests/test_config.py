import unittest

from pwapt import Config

TEST_SETTING = True
no_go_here = True


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_config_from_dict(self):
        config_dict = {
            'DEBUG': True,
            'SAMPLING_INTERVAL': 0.001,
        }
        self.config.from_dict(config_dict)

        self.assertIn('DEBUG', self.config.keys())
        self.assertIn('SAMPLING_INTERVAL', self.config.keys())

        self.assertEqual(self.config['DEBUG'], True)
        self.assertEqual(self.config['SAMPLING_INTERVAL'], 0.001)

    def test_config_from_object(self):
        class ConfigObject(object):
            SAMPLING_INTERVAL = 0.001
            DEBUG = True
            no_go_here = True

        self.config.from_object(ConfigObject)

        self.assertIn('SAMPLING_INTERVAL', self.config.keys())
        self.assertNotIn('no_go_here', self.config.keys())
        self.assertEqual(self.config['SAMPLING_INTERVAL'], 0.001)

    def test_all_uppercase(self):
        config_dict = {
            'DEBUG': True,
            'no_go_here': True,
            'SAMPLING_INTERVAL': 0.001
        }
        self.config.from_dict(config_dict)

        self.assertNotIn('no_go_here', self.config.keys())
        self.assertIn('DEBUG', self.config.keys())
        self.assertIn('SAMPLING_INTERVAL', self.config.keys())

    def test__get_valid_keys(self):
        key_dict = {
            "nope": 0,
            "__NOPE__": 0,
            "THIS_WORKS": 1,
        }
        keys = self.config._get_valid_keys(key_dict)

        self.assertNotIn("nope", keys)
        self.assertNotIn("__NOPE__", keys)
        self.assertIn("THIS_WORKS", keys)
