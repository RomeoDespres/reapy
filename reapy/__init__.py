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
from .tools import InsideReaper


def inside_reaper():
    """
    Return context manager for efficient calls from outside REAPER.
    
    Returns
    -------
    inside_reaper : InsideReaper
    
    Examples
    --------
    Instead of running:
    
    >>> project = reapy.Project()
    >>> l = [project.bpm for i in range(1000)
    
    which takes around 30 seconds, run:
    
    >>> project = reapy.Project()
    >>> with reapy.inside_reaper():
    ...     l = [project.bpm for i in range(1000)
    ...
    
    which takes 0.1 seconds!
    """
    return InsideReaper()