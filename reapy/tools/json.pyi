"""Encode and decode ``reapy`` objects as JSON."""

import importlib
import json
import operator
import sys
import types
import typing as ty

T1 = ty.TypeVar('T1')


class ClassCache(ty.Dict[str, T1]):

    _module_name: str
    _module: ty.Optional[types.ModuleType] = None

    def __missing__(self, key: str) -> T1:
        ...


class GuiCache(ClassCache[T1]):
    ...


class JSCache(ClassCache[T1]):
    ...


_CLASS_CACHE: ClassCache[object]
_GUI_CACHE: GuiCache[object]
_JS_CACHE: JSCache[object]


class ReapyEncoder(json.JSONEncoder):
    def default(self, x: ty.Any) -> ty.Any:
        ...


def loads(s: ty.Union[ty.Text, bytes]) -> ty.Any:
    ...


def dumps(x: ty.Any) -> str:
    ...


def object_hook(x: ty.Any) -> ty.Any:
    ...
