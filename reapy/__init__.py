import sys


def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.

    If ``reapy`` is run from inside a REAPER instance but currently
    controls another REAPER instance on a slave machine (with
    ``reapy.machines.select_machine``), return False.
    """
    inside = hasattr(sys.modules["__main__"], "obj")
    if not inside:
        return False
    else:
        try:
            return machines.get_selected_machine_host() is None
        except NameError:
            # machines is undefined because we are still in the initial
            # import process.
            return True



from .tools import (
    connect, connect_to_default_machine, dist_api_is_enabled, inside_reaper,
    reconnect
)
from . import reascript_api
from .core import *
from .core.reaper import *


__version__ = "0.7.1"
