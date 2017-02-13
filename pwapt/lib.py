"""Helper classes and functions."""


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
        if obj is None:
            return self
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
