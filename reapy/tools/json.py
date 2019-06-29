"""Encode and decode ``reapy`` objects as JSON."""

import importlib
import json


class ClassCache(dict):

    _core = None

    def __missing__(self, key):
        if self._core is None:
            # The import is here because otherwise there is an import loop
            # and to perform import just once.
            self._core = importlib.import_module("reapy.core")
        self[key] = getattr(self._core, key)
        return self[key]


_CLASS_CACHE = ClassCache()


class ReapyEncoder(json.JSONEncoder):

    def default(self, x):
        if hasattr(x, '_to_dict'):
            return x._to_dict()
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if "__reapy__" not in x:
        return x
    reapy_class = _CLASS_CACHE[x["class"]]
    return reapy_class(*x["args"], **x["kwargs"])
