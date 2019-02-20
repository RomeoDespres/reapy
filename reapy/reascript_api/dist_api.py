import reapy


if not reapy.is_inside_reaper():
    try:
        from reapy.tools import Program
        import sys, tempfile
        sys.path.append(tempfile.gettempdir())
        from reapy_generated_api import __all__
        from reapy_generated_api import *
    except ImportError:
        __all__ = []

