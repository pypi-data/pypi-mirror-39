#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import argparse
import collections
import operator

from accessor.accessors import FailLoudAccessor


# ================================================================================
# data structures for configuration object
# ================================================================================

class Tree(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._store = dict(*args, **kwargs)

    def __getitem__(self, key):
        if key not in self._store:
            self._store[key] = Tree()

        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __getattr__(self, key):
        if key.startswith('_'):
            return object.__getattr__(self, key)
        else:
            return self.__getitem__(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)

    def freeze(self):
        return self._freeze_value(self._store)

    @classmethod
    def _freeze_value(cls, value):
        if isinstance(value, collections.Mapping):
            return Namespace(**{k: cls._freeze_value(value[k]) for k in value})
        elif isinstance(value, collections.Collection) and (not isinstance(value, str)):
            return tuple(cls._freeze_value(v) for v in value)
        else:
            return value


class Namespace(argparse.Namespace):
    def get(self, path, default=None):
        try:
            return FailLoudAccessor(path).resolve(self)
        except ValueError:
            return default

    def has(self, path):
        try:
            FailLoudAccessor(path).resolve(self)
            return True
        except ValueError:
            return False


# ================================================================================
# object proxy
# ================================================================================

class ObjectProxy(object):
    def _new_method_proxy(func):
        def inner(self, *args, **kwargs):
            return func(self._get_proxy_target(), *args, **kwargs)

        return inner

    def __init__(self, getter):
        self._get_proxy_target = getter

    def __setattr__(self, name, value):
        if name == '_get_proxy_target':
            self.__dict__['_get_proxy_target'] = value
        else:
            setattr(self._get_proxy_target(), name, value)

    __getattr__ = _new_method_proxy(getattr)
    __delattr__ = _new_method_proxy(delattr)

    __bytes__ = _new_method_proxy(bytes)
    __str__ = _new_method_proxy(str)
    __bool__ = _new_method_proxy(bool)

    __dir__ = _new_method_proxy(dir)

    __class__ = property(_new_method_proxy(operator.attrgetter('__class__')))
    __eq__ = _new_method_proxy(operator.eq)
    __ne__ = _new_method_proxy(operator.ne)
    __hash__ = _new_method_proxy(hash)

    __getitem__ = _new_method_proxy(operator.getitem)
    __setitem__ = _new_method_proxy(operator.setitem)
    __delitem__ = _new_method_proxy(operator.delitem)

    __len__ = _new_method_proxy(len)
    __contains__ = _new_method_proxy(operator.contains)

    __call__ = property(_new_method_proxy(operator.attrgetter('__call__')))
