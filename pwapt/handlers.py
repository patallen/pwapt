
import collections
from abc import ABCMeta, abstractmethod


from pwapt import callstack as cs


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

    This class should do all the work of ordering/formatting
    the samples as desired. In this implimentation we are just
    keeping an aggregate count of each formatted call.
    """

    stack_class = cs.CallStack

    def __init__(self):
        self.store = collections.defaultdict(int)

    def handle(self, sample):
        """Increment the count for this stack hash."""

        callstack = self.stack_class.from_frame(frame=sample)
        self.store[callstack] += 1

    def dump(self, reset=False):
        """Return our the the dict as-is."""
        return self.store

    def reset(self):
        """Drop all of our current samples and reset the timer."""
        self.store = collections.defaultdict(int)

    @property
    def sample_count(self):
        """How many samples we have handled since the last timer reset."""
        return sum(self.store.values())

    def __contains__(self, other):
        return other in [hash(cs) for cs in self.store.keys()]
