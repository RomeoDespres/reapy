"""
Enable ```reapy`` distant API.

Running this ReaScript from inside REAPER allows to import ``reapy``
from outside. It creates a persistent Web Interface inside REAPER and
adds the ReaScript ``reapy.reascripts.activate_reapy_server`` to the
Actions list. Importing ``reapy`` from outside REAPER will trigger
the latter **via** the Web Interface.
"""
import os

if __name__ == "__main__":
    import reapy
    reapy.config.enable_dist_api()
    from reapy.core.gui import _JS_generator
    api_filepath = "{root}{s}JS_API.py".format(
        root=os.path.dirname(_JS_generator.__file__), s=os.sep)
    bin_dir = "{root}{s}UserPlugins{s}".format(
        root=reapy.get_resource_path(), s=os.sep)
    # print(api_filepath)
    # print(bin_dir)
    _JS_generator.generate_js_api(bin_dir, api_filepath)
