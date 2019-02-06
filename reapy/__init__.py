import sys

# Whether reapy is imported from inside REAPER.
def is_inside_reaper():
    inside = hasattr(sys.modules["__main__"], "obj")
    return inside

from . import reascript_api
from .core.project import Project
from .core.reaper import *

CURRENT_PROJECT = Project(0)

def enable_dist_api(web_interface_port=2307, reapy_server_port=2308):
    ini_path = get_config()
    
def disable_dist_api():
    pass
