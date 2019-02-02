import sys

_running_from_reaper = hasattr(sys.modules["__main__"], "obj")

if _running_from_reaper:
    # Import functions without the useless starting "RPR_".
    import reaper_python as _RPR
    for key in _RPR.__dict__:
        if key.startswith("RPR_"):
            exec("{} = _RPR.__dict__['{}']".format(key[4:], key))
else:
    from .dist_api import *
