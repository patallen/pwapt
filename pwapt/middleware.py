from lib import import_from_string
from pwapt.exceptions import PwaptConfigException


class MiddlewareManager(object):
    """Base MiddlewareManager.

    Allows us to set up middleware from the config.
    """

    CONFIG_NAME = None
    METHOD_STRING = None

    def __init__(self, *middlewares):
        """Init with imported middleware classes."""
        self.middleware_classes = []

        for mw_class in middlewares:
            self._add_middleware(mw_class)

    @classmethod
    def from_config(cls, config):
        """Load middleware classes and use to instantiate."""
        config = config.get(cls.CONFIG_NAME)
        middleware_classes = cls._get_mw_classes_from_config(config)
        return cls(*middleware_classes)

    @classmethod
    def _get_mw_class_from_string(cls, string):
        return import_from_string(string)

    @classmethod
    def _get_mw_classes_from_config(cls, config):
        imports = []
        try:
            for import_string in config:
                imp = cls._get_mw_class_from_string(import_string)
                imports.append(imp)
        except TypeError:
            raise PwaptConfigException(
                "No config for %s found. Make sure to include a %s entry in "
                "your config." % (cls.MIDDLEWARE_TYPE, cls.CONFIG_NAME)
            )

        return imports

    def _add_middleware(self, mw_class):
        try:
            res = hasattr(mw_class, self.METHOD_STRING)
            if not res:
                raise AttributeError(
                    'This middleware requries a method named %s.' %
                    self.METHOD_STRING
                )
        except TypeError:
            raise TypeError(
                "%s.METHOD_STRING must be a string." %
                (self.__class__.__name__)
            )
        self.middleware_classes.append(mw_class)


class SamplerMiddlewareManager(MiddlewareManager):
    """Manager for middleware between the Sampler and the Handler."""

    MIDDLEWARE_TYPE = 'SamplerMiddleware'
    CONFIG_NAME = 'SAMPLER_MIDDLEWARE_CLASSES'
    METHOD_STRING = 'process_sample'

    def process_sample(self, sample):
        """Apply all of the middlewares to the sample."""
        for middleware_class in self.middleware_classes:
            mw = middleware_class()
            sample = mw.process_sample(sample)
        return sample


class HandlerMiddlewareManager(MiddlewareManager):
    """Manager for middleware between the Handler and the Finaler."""

    MIDDLEWARE_TYPE = 'HandlerMiddleware'
    CONFIG_NAME = 'HANDLER_MIDDLEWARE_CLASSES'
    METHOD_STRING = 'process_payload'

    def process_payload(self, payload):
        """Apply all of the middlewares to the payload."""
        for middleware_class in self.middleware_classes:
            mw = middleware_class()
            payload = mw.process_payload(payload)
        return payload
