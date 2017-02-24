import time
import signal
import atexit
from pwapt.middleware import SamplerMiddlewareManager


class Sampler(object):
    """Takes samples of the current stack at `interval`.

    The sampler is completely output-agnostic. It simply samples at the given
    interval and hands the sample (Frame) off to the specified handler_class to
    deal with as desired.
    """

    def __init__(self, handler, config):
        """Intialize the sampler - set interval and create handler."""
        self.middleware = SamplerMiddlewareManager.from_config(config)
        self.interval = config['SAMPLING_INTERVAL']
        self.handler = handler
        self._started_at = None
        self._last_reset = None

    def start(self):
        """Start the sampling loop and timers as necessary."""
        self.reset()
        if self._started_at is None:
            self._started_at = time.time()

        try:
            signal.signal(signal.SIGVTALRM, self._sample)
        except ValueError:
            raise ValueError('Can only sample on the main thread')

        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)
        atexit.register(self.stop)

    def _sample(self, signum, frame):
        sample = self.middleware.process_sample(frame)
        self.handler.handle(sample)
        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval)

    def reset(self):
        """Reset the handler and last restart time."""
        self.handler.reset()
        self._last_reset = time.time()

    def stop(self):
        """Stop the operation of the sampler.

        This resets the handler and sets nullifies _started_at
        """
        self.reset()
        self._startd_at = None
        signal.setitimer(signal.ITIMER_VIRTUAL, 0)

    def __del__(self):
        """Stop the signals when the object is deleted.

        This prevents any signal timeout exceptions from being raised.
        """
        self.stop()

    @property
    def session_duration(self):
        """How long we've been running since the last reset call."""
        if self._last_reset is None:
            return 0
        return time.time() - self._last_reset

    @property
    def total_duration(self):
        """How long we've been running since `start` was called."""
        if self._started_at is None:
            return 0
        return time.time() - self._started_at
