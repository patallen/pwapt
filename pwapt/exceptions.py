class PwaptException(BaseException):
    """Generic Pwapt base exception."""

    pass


class PwaptConfigException(PwaptException):
    """Throw this exception when the config is not valid."""

    MISSING_REQUIRED = 'Missing required config options.'
    MISSING_CONFIG = 'No configuration has been defined.'
    INVALID_VALUE = 'Invalid configuration value.'
