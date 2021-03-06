import time

from pwapt.config import Config

from pwapt.sampler import Sampler as DefaultSampler
from pwapt.handlers import SampleHandler as DefaultHandler

from pwapt import exceptions as exc
import gevent


class Pwapt(object):
    """This is the main class.

    The Pwapt object is responsible for dispatching the sampler
    and handler, setting up middleware, and handling the config.

    On :meth: `run`, it will return an interface to which you
    can safely interact with the handler & sampler.
    """

    DEFAULT_SAMPLER_CLASS = DefaultSampler
    DEFAULT_HANDLER_CLASS = DefaultHandler

    def __init__(self):
        self.config = Config()
        self.handler_middlewares = []
        self._started = False
        self.sampler = None
        self.handler = None

    def run(self):
        """Start the sampler after checking configs."""
        self._validate_config()

        self.handler = self._make_handler()
        self.sampler = self._make_sampler(self.handler)

        gevent.spawn(self.sampler.start)

        self._started = time.time()

    def _validate_config(self):
        if not self.config.keys():
            raise exc.PwaptConfigException(
                exc.PwaptConfigException.MISSING_CONFIG)
        for req in self.config.__required_keys__:
            if req not in self.config.keys():
                raise exc.PwaptConfigException(
                    exc.PwaptConfigException.MISSING_REQUIRED)

    def _make_handler(self):
        class_ = self.config.get('handler_class') or self.DEFAULT_HANDLER_CLASS
        return class_(config=self.config)

    def _make_sampler(self, handler):
        class_ = self.config.get('sampler_class') or self.DEFAULT_SAMPLER_CLASS
        return class_(handler=handler, config=self.config)
