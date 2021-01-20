"""Encode and decode ``reapy`` objects as JSON."""

import importlib
import json
import operator
import sys


class ClassCache(dict):
    _module_name = "reapy.core"
    _module = None

    def __missing__(self, key):
        if self._module is None:
            # The import is here because otherwise there is an import loop
            # and to perform import just once.
            self._module = importlib.import_module(self._module_name)
        self[key] = getattr(self._module, key)
        return self[key]


class GuiCache(ClassCache):
    _module_name = "reapy.core.gui"

class GuiJSCache(ClassCache):
    _module_name = "reapy.core.gui.JS_API"


_CLASS_CACHE = ClassCache()
_GUI_CACHE = GuiCache()
_GUI_JS_CACHE = GuiJSCache()


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
        elif isinstance(x, slice):
            return {"__slice__": True, "args": (x.start, x.stop, x.step)}
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if "__reapy__" in x:
        if "JS_API" in x["module"]:
            reapy_class = _GUI_JS_CACHE[x["class"]]
        elif x["module"].startswith("reapy.core.gui"):
            reapy_class = _GUI_CACHE[x["class"]]
        else:
            reapy_class = _CLASS_CACHE[x["class"]]
        obj = reapy_class(*x["args"], **x["kwargs"])
        obj.state = x["state"]
        return obj
    elif "__callable__" in x:
        module_name, name = x["module_name"], x["name"]
        try:
            module = sys.modules[module_name]
        except KeyError:
            module = importlib.import_module(module_name)
        return operator.attrgetter(name)(sys.modules[module_name])
    elif "__slice__" in x:
        return slice(*x["args"])
    else:
        return x
