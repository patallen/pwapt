import time
import signal
import atexit


from pwapt.handlers import SampleHandler


class Sampler(object):
    """Takes samples of the current stack at `interval`.

    The sampler is completely output-agnostic. It simply samples at the given
    interval and hands the sample (Frame) off to the specified handler_class to
    deal with as desired.
    """

    def __init__(self, interval, handler_class):
        """Intialize the sampler - set interval and create handler."""
        if not issubclass(handler_class, SampleHandler):
            raise ValueError(
                '`handler_class` must be a subclass of SampleHandler'
            )
        self.interval = interval
        self.handler = handler_class()
        self._started_at = None
        self._last_restart = None

    def start(self):
        """Start the sampling loop."""
        self._started_at = time.time()
        try:
            signal.signal(signal.SIGVTALRM, self._sample)
        except ValueError:
            raise ValueError('Can only sample on the main thread')

        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)
        atexit.register(self.stop)

    def _sample(self, signum, frame):
        self.handler.handle(frame)
        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)

    def reset(self):
        self.handler.reset()
        self._started_at = time.time()

    def stop(self):
        self.reset()
        self._startd_at = None
        signal.setitimer(signal.ITIMER_VIRTUAL, 0)

    def __del__(self):
        self.stop()

    def dump(self, reset=False):
        return self.handler.dump(reset=reset)

    @property
    def session_duration(self):
        if not self._last_restart:
            return 0
        return time.time() - self._last_restart

    @property
    def total_duration(self):
        if not self._started_at:
            return 0
        return time.time() - self._started_at
