import sys


def is_inside_reaper() -> bool:
    """
    Return whether ``reapy`` is imported from inside REAPER.
    """
    ...


from .tools import inside_reaper
from . import reascript_api
from .core import *
from .core.reaper import *
