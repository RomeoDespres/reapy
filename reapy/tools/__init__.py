"""Define tools such as Program and custom json module."""

import reapy
if not reapy.is_inside_reaper():
    from .dist_program import Program
else:
    from .program import Program
