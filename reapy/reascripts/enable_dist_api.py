"""
Enable ```reapy`` distant API.

Running this ReaScript from inside REAPER allows to import ``reapy``
from outside. It creates a persistent Web Interface inside REAPER and
adds the ReaScript ``reapy.reascripts.activate_reapy_server`` to the
Actions list. Importing ``reapy`` from outside REAPER will trigger
the latter **via** the Web Interface.
"""
import os
import traceback
from sys import exc_info
from sys import stdout

if __name__ == "__main__":
    try:
        import reapy
    except Exception as e:
        traceback.print_tb(exc_info()[2], file=stdout)
        print(e)
    reapy.config.enable_dist_api()
    from reapy.core.gui import _JS_generator
    api_filename = "_JS_API_generated.py"
    bin_dir = os.path.join(reapy.get_resource_path(), "UserPlugins")
    _JS_generator.generate_js_api(bin_dir, api_filename)
