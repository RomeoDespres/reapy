import sys

_running_from_reaper = hasattr(sys.modules["__main__"], "obj")

if _running_from_reaper:
	from reaper_python import *
else:
	from .dist_api import *