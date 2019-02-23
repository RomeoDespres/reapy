import sys


def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.
    """
    inside = hasattr(sys.modules["__main__"], "obj")
    return inside


from . import config, reascript_api
from .core import *
from .core.reaper import *
from .tools import InsideReaper as inside_reaper
