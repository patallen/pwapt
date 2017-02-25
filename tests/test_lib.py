import unittest
import time
from pwapt.lib import import_from_string, cachedproperty


class TestClass(object):
    @cachedproperty
    def this_should_cache(self):
        return time.time()


@cachedproperty
def hello():
    return "hello"


class LibTestCase(unittest.TestCase):
    def setUp(self):
        self.testclass = TestClass()

    def test_cached_property_caches(self):
        t = self.testclass.this_should_cache

        self.assertEqual(t, self.testclass.this_should_cache)

    def test_import_from_string_works(self):
        random = import_from_string('random.random')

        try:
            rand = random()
        except NameError:
            self.fail("myFunc() raised ExceptionType unexpectedly!")

        self.assertIsNotNone(rand)

    def test_bad_import_string(self):
        with self.assertRaises(ImportError):
            import_from_string('kdsjdalfjalk')

    def test_bad_function(self):
        with self.assertRaises(ImportError):
            import_from_string('random.xyzabcnope')

    def test_no_self(self):
        rv = hello
        self.assertIsInstance(rv, cachedproperty)
