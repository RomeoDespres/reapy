"""Encode and decode ``reapy`` objects as JSON."""

import importlib
import json
import operator
import sys


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
        elif callable(x):
            return {
                "__callable__": True,
                "module_name": x.__module__,
                "name": x.__qualname__
            }
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if "__reapy__" in x:
        reapy_class = _CLASS_CACHE[x["class"]]
        return reapy_class(*x["args"], **x["kwargs"])
    elif "__callable__" in x:
        module_name, name = x["module_name"], x["name"]
        try:
            module = sys.modules[module_name]
        except KeyError:
            module = importlib.import_module(module_name)
        return operator.attrgetter(name)(sys.modules[module_name])
    else:
        return x
