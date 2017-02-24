"""This module contains Classes that represent the call stack."""


class CallStack(object):
    """Represents the entire call stack for any given sample.

    The call stack is not responsible for much other than holding
    creating an instance of itself and holding the stack frames.
    """

    def __init__(self, frames):
        """Initialize and store a set of stack frames."""
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
