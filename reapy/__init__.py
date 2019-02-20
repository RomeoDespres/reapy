import sys

# Whether reapy is imported from inside REAPER.
def is_inside_reaper():
    inside = hasattr(sys.modules["__main__"], "obj")
    return inside

from . import config, reascript_api
from .core import *
from .core.reaper import *
