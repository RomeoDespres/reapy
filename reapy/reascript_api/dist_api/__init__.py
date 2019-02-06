import reapy

if not reapy.is_inside_reaper():
    from . import api_function
    import sys, tempfile
    sys.path.append(tempfile.gettempdir())
    from reapy_generated_api import *


