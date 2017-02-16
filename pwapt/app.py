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
        sampler_class = self._get_sampler_class()
        handler_class = self._get_handler_class()
        sampler, handler = _setup_and_start(sampler_class=sampler_class,
                                            handler_class=handler_class,
                                            config=self.config)
        self.sampler, self.handler = sampler, handler
        self._started = time.time()
        # return PwaptInterface(self, sampler, handler)

    def _validate_config(self):
        if not self.config.keys():
            raise exc.PwaptConfigException(
                exc.PwaptConfigException.MISSING_CONFIG)
        for req in self.config.__required_keys__:
            if req not in self.config.keys():
                raise exc.PwaptConfigException(
                    exc.PwaptConfigException.MISSING_REQUIRED)

    def _get_handler_class(self):
        return self.config.get('handler_class') or self.DEFAULT_HANDLER_CLASS

    def _get_sampler_class(self):
        return self.config.get('sampler_class') or self.DEFAULT_SAMPLER_CLASS


def _setup_and_start(sampler_class, handler_class, config):
    handler = handler_class(config=config)
    sampler = sampler_class(handler=handler, config=config)

    def run_sampler(sampler):
        sampler.start()
    gevent.spawn(run_sampler, sampler)
    return sampler, handler
