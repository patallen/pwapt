import collections
import copy
import warnings
import time

from abc import ABCMeta, abstractmethod

from pwapt import callstack as cs
from pwapt import middleware as mw


class BaseSampleHandler:
    """Abstract base class for handling samples.

    This class should do all the work of ordering/formatting
    the samples as desired.
    """

    __metaclass__ = ABCMeta

    stack_class = None

    @abstractmethod
    def handle(self):
        """Method used by the Sampler to hand over samples."""
        pass

    @abstractmethod
    def reset(self):
        """Method used by the Sampler to drop the sample set."""
        pass

    @abstractmethod
    def dump(self):
        """Method used by the Sampler to retrive the data."""
        pass


class SampleHandler(BaseSampleHandler):
    """"Handles and stores samples provided by the Sampler.

    This class is only responsible for storing the call stacks
    and their counts and handing the data over when requested.
    """

    stack_class = cs.CallStack

    def __init__(self, config):
        """Initialize the sampler and any middleware."""
        self.middleware = mw.HandlerMiddlewareManager.from_config(config)
        self.store = collections.defaultdict(int)
        self._dump_interval = config['HANDLER_DUMP_INTERVAL']

    def handle(self, sample):
        """Increment the count for this stack hash."""
        callstack = self.stack_class.from_frame(frame=sample)
        self.store[callstack] += 1
        if self._dump_interval and self.last_reset_delta > self._dump_interval:
            self.dump()

    def dump(self):
        """Return our the the dict as-is."""
        store = copy.copy(self.store)
        dump = self.middleware.process_payload(store)
        self.reset()
        return dump

    def reset(self):
        """Drop all of our current samples and reset the timer."""
        self._last_reset = time.time()
        self.store = collections.defaultdict(int)

    @property
    def sample_count(self):
        """How many samples we have handled since the last timer reset."""
        return sum(self.store.values())

    @property
    def last_reset_delta(self):
        return time.time() - self._last_reset

    def __contains__(self, other):
        """Check hash of `other` call stack against the ones in the store."""
        return other in [hash(cs) for cs in self.store.keys()]
