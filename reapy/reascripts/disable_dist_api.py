"""
Disable ```reapy`` distant API.

Running this ReaScript from inside REAPER disables ``reapy`` imports
from outside. It deletes the persistent Web Interface and removes the
ReaScript ``reapy.reascripts.activate_reapy_server`` from the Actions
list.

See also
--------
reapy.reascripts.enable_dist_api
"""

if __name__ == "__main__":
    import reapy
    reapy.config.disable_dist_api()
