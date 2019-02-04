import sys

# Whether reapy is imported from inside REAPER.
_INSIDE = hasattr(sys.modules["__main__"], "obj")

from . import reascript_api
from .core.project import Project
from .core.reaper import *

CURRENT_PROJECT = Project(0)
