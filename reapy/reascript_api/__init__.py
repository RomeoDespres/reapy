import reapy

import sys

<<<<<<< HEAD
if reapy.is_inside_reaper():
=======
if reapy._INSIDE:
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
    # Import functions without the useless starting "RPR_".
    import reaper_python as _RPR
    for key in _RPR.__dict__:
        if key.startswith("RPR_"):
            exec("{} = _RPR.__dict__['{}']".format(key[4:], key))
    __all__ = list(_RPR._ft)
else:
    from .dist_api import *
    __all__ = reapy.reascript_api.dist_api.generated_api.__all__
