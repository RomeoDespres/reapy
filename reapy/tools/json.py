"""Encode and decode ``reapy`` objects as JSON."""

import importlib
import json
import operator
import sys


class ClassCache(dict):

    _core = None
    _modules = {}
    _classes = {}

    def __missing__(self, key):
        if self._core is None:
            # The import is here because otherwise there is an import loop
            # and to perform import just once.
            self._core = importlib.import_module("reapy.core")
        self[key] = getattr(self._core, key)
        return self[key]

    def with_module(self, module, class_):
        """Try to reimport subclass from the outer package.

        Parameters
        ----------
        module : str
            cached module name
        class_ : str
            cached class name

        Returns
        -------
        Type
            class object

        Raises
        ------
        ImportError
            If outer module can't be accesed from Python PATH
        """
        key = '{}.{}'.format(module, class_)
        if key in self._classes:
            return self._classes[key]
        if module not in self._modules:
            try:
                self._modules[module] = importlib.import_module(module)
            except ImportError as e:
                raise ImportError('Probably, your script is not installed as'
                                  ' package and/or not in the Python PATH.\n'
                                  'Original exception:\n%s' % e)
        self._classes[key] = getattr(self._modules[module], class_)
        return self._classes[key]


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
        elif isinstance(x, slice):
            return {"__slice__": True, "args": (x.start, x.stop, x.step)}
        return json.JSONEncoder.default(self, x)


def loads(s):
    return json.loads(s, object_hook=object_hook)


def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)


def object_hook(x):
    if "__reapy__" in x:
        if not x["module"].startswith("reapy"):
            reapy_class = _CLASS_CACHE.with_module(x["module"], x["class"])
        else:
            reapy_class = _CLASS_CACHE[x["class"]]
        return reapy_class(*x["args"], **x["kwargs"])
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
