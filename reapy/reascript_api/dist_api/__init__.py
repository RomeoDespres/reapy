import reapy

if not reapy.is_inside_reaper():
    from .generated_api import *


