import reapy

import sys

if reapy.is_inside_reaper():
    # Import functions without the useless starting "RPR_".
    import reaper_python as _RPR
    __all__ = [s[4:] for s in _RPR.__dict__ if s.startswith("RPR_")]
    for s in __all__:
        exec("{} = _RPR.__dict__['{}']".format(s, "RPR_" + s))
    # Import SWS functions.
    try:
        import sws_python as _SWS
        sws_functions = set(_SWS.__dict__) - set(_RPR.__dict__)
        __all__ += list(sws_functions)
        for s in sws_functions:
            exec("from sws_python import {}".format(s))
    except ModuleNotFoundError:  # SWS is not installed
        pass
else:
    from .dist_api import __all__
    from .dist_api import *
