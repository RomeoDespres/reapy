import reapy

import sys

if reapy.is_inside_reaper():
    # Import functions without the useless starting "RPR_".
    import reaper_python as _RPR
    for key in _RPR.__dict__:
        if key.startswith("RPR_"):
            exec("{} = _RPR.__dict__['{}']".format(key[4:], key))

    # Import SWS functions.
    try:
        import sws_python as _SWS
        for key in _SWS.__dict__:
            if key not in _RPR.__dict__:
                exec("from sws_python import {}".format(key))
    except ModuleNotFoundError:
        pass
    __all__ = list(_RPR._ft)
else:
    from .dist_api import __all__
    from .dist_api import *
