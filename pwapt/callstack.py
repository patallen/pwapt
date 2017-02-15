"""
This module contains Classes that represent the call stack.

A CallStack object doesn't do much other than format it's output
as desired based on :meth: format_stack and :meth: format_frame.
"""

class CallStack(object):
    def __init__(self, frames):
        self.frames = frames

    @classmethod
    def from_frame(cls, frame):
        """Create a CallStack instance given the top-most Frame."""
        rv = []
        while frame is not None:
            rv.append(frame)
            frame = frame.f_back
        callstack = cls(frames=[f for f in reversed(rv)])
        return callstack

    @property
    def depth(self):
        """Return how many frames are in the callstack."""
        return len(self.frames)

    def __repr__(self):
        """Represent by the code names joined with ;."""
        names = [str(f.f_code.co_name) for f in self.frames]
        return ";".join(names)

    def __hash__(self):
        """Hash based on the frame filenames."""
        hash_ = hash("".join([str(f.f_code.co_filename) for f in self.frames]))
        return hash_

    def __eq__(self, other):
        """Equal by hash."""
        return hash(self) == hash(other)


class FlameGraphCallStack(CallStack):
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
