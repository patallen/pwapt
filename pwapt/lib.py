"""Helper classes and functions."""
from importlib import import_module


class cachedproperty(object):
    """Caching decorator for methods that take no args.

    This should be used in place of @property when there is
    the opportunity to cache the return value.
    """

    def __init__(self, func):
        """Ensure that docstrings are preserved."""
        self.func = func
        self.f_name = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, _cls):
        """Get the value from the cache or evaluate the func."""
        ev = self._prop_cache(obj).get(self.f_name)
        return ev or self._cache_and_return(obj)

    def _prop_cache(self, obj):
        if not hasattr(obj, '_prop_cache'):
            obj._prop_cache = {}
        return obj._prop_cache

    def _cache_and_return(self, obj):
        rv = self.func(obj)
        self._prop_cache(obj)[self.f_name] = rv
        return rv


def import_from_string(dotted_path):
    """Import a module based on a given string.

    Used primarily for middleware. Borrowed from Django.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError("Not a module path.")

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module "%s" does not define a "%s"' % (
            module_path, class_name)
        )
