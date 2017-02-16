"""Sample Middleware.

To use any of these, add 'pwapt.contrib.middleware.<classname>'
to their respective spots in your Pwapt config.
"""

import sys
import time


class DumpLoggingMiddleware(object):
    """Handler Middleware that logs dump stats to stdout."""

    def process_payload(self, payload):
        """Let's display the size of the payload."""
        count = sum(payload.values())
        length = len(payload)
        size = sys.getsizeof(payload)
        print "Dumped %s samples in %s unique groups. Size: %s bytes." % (
            count, length, size
        )
        return payload


class FormattingHandlerMiddleware(object):
    """Format callstacks into (timestamp, count, stack-string) format.

    This would fit nicely with a second handler to push to a DB.
    """

    def process_payload(self, payload):
        def format_frame(frame):
            return "%s(%s)" % (
                frame.f_code.co_name,
                frame.f_globals.get('__name__')
            )
        ts = time.time()
        rv = []
        for callstack, count in payload.iteritems():
            string = ";".join([format_frame(f) for f in callstack.frames])
            rv.append((ts, count, string))
        return rv
