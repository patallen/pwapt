"""
This module contains Classes that represent the call stack.

A CallStack object doesn't do much other than format it's output
as desired based on :meth: format_stack and :meth: format_frame.
"""

from abc import ABCMeta, abstractmethod

from lib import cachedproperty


class CallStack:
    """Base class that represensts a call stack as a whole."""

    __metaclass__ = ABCMeta

    def __init__(self, frame):
        """Save the top frame for later."""
        self._top_frame = frame

    @abstractmethod
    def format_stack(self, frame):
        """Format the entire entire stack as a string."""
        pass

    @abstractmethod
    def format_frame(self, frame):
        """Format a single frame as a string."""
        pass

    @cachedproperty
    def formatted(self):
        """Return the final format of the callstack as a string."""
        return self.format_stack(self.frames)

    @cachedproperty
    def frames(self):
        """Back into a list of frames from the top frame."""
        rv = []
        frame = self._top_frame
        while frame is not None:
            rv.append(frame)
            frame = frame.f_back
        return list(reversed(rv))

    def __repr__(self):
        return self.formatted

    def __str__(self):
        return self.formatted

    def __eq__(self, other):
        """Equal if :property: formatted's are equal."""
        return self.formatted == other.formatted


class FlameGraphFormatMixin(object):
    """Formatter for FlameGraph output.

    Each frame is formatted as:
        "modulename`function_name"

    Each frame in the final format is joined by ';'
    """

    def format_frame(self, frame):
        """Format each frame as "module.__name__`function_name"."""
        name = frame.f_code.co_name
        filename = frame.f_globals.get('__name__')
        return "%s`%s" % (filename, name)

    def format_stack(self, frames):
        """Format the stack by joining the formatted frames on ';'."""
        return ";".join(map(self.format_frame, frames))


class FlameGraphCallStack(FlameGraphFormatMixin, CallStack):
    """Callstack that formats output in the Flamegraph format."""

    pass
