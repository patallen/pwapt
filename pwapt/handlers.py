
import collections
from abc import ABCMeta, abstractmethod


from pwapt.callstack import FlameGraphCallStack


class SampleHandler:
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


class FlameGraphSampleHandler(SampleHandler):
    """"Handles and stores samples provided by the Sampler.

    This class should do all the work of ordering/formatting
    the samples as desired. In this implimentation we are just
    keeping an aggregate count of each formatted call.
    """

    stack_class = FlameGraphCallStack

    def __init__(self):
        self._cache = collections.defaultdict(int)

    def handle(self, sample):
        """Increment the count for this stack hash."""
        self._cache[str(self.stack_class(sample))] += 1

    def dump(self, reset=False):
        """Return our the the dict as-is."""
        return self._cache

    def reset(self):
        """Drop all of our current samples and reset the timer."""
        self._cache = collections.defaultdict(int)

    @property
    def sample_count(self):
        """How many samples we have handled since the last timer reset."""
        return sum(self._cache.values())
