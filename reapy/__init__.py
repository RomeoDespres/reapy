import sys

# Whether reapy is imported from inside REAPER.
def is_inside_reaper():
    inside = hasattr(sys.modules["__main__"], "obj")
    return inside

from . import config, reascript_api
from .core.project import Project
from .core.reaper import *

CURRENT_PROJECT = Project(0)