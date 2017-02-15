
class Config(dict):
    """Configuration object that operaties like a dict.

    Setting names must be CAPITALIZED and must starte with
    a letter else they will not be included in the config.
    """

    def from_dict(self, conf_dict):
        """Populate the config from a python dictionary."""
        keys = self._get_valid_keys(conf_dict)
        for k in keys:
            self[k] = conf_dict[k]

    def from_object(self, conf_object):
        """Populate the config from a python Class."""
        keys = self._get_valid_keys(vars(conf_object))
        for key in keys:
            self[key] = getattr(conf_object, key)

    def _get_valid_keys(self, adict):
        rv = []
        for key in adict.keys():
            if key.startswith('_') or not key.isupper():
                continue
            rv.append(key)
        return rv
