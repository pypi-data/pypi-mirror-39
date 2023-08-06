from importlib import import_module

from django.utils.encoding import smart_text
from django.core.exceptions import ImproperlyConfigured
integer_types = (int,)
    

class CacheKey(object):
    """
    A stub string class that we can use to check if a key was created already.
    """
    def __init__(self, key):
        self._key = key

    def __str__(self):
        return smart_text(self._key)

    def original_key(self):
        key = self._key.rsplit(":", 1)[1]
        return key
    

def load_class(path):
    """通过路径加载类"""

    mod_name, klass_name = path.rsplit('.', 1)

    try:
        mod = import_module(mod_name)
    except AttributeError as e:
        raise ImproperlyConfigured('Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured('Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))

    return klass


def default_reverse_key(key):
    return key.split(':', 2)[2]

