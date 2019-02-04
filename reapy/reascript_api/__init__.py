import reapy

import sys

if reapy._INSIDE:
    # Import functions without the useless starting "RPR_".
    import reaper_python as _RPR
    for key in _RPR.__dict__:
        if key.startswith("RPR_"):
            exec("{} = _RPR.__dict__['{}']".format(key[4:], key))
else:
    from .dist_api import *
