"""Get setup infos."""

from reapy.reascripts import enable_dist_api, disable_dist_api

import os
import sys


def get_config_scripts():
    """
    Return paths to configuration ReaScripts.
    """
    return (
        os.path.abspath(enable_dist_api.__file__),
        os.path.abspath(disable_dist_api.__file__)
    )


def get_python_dll():
    """
    Return path to Python DLL (if it can be found).
    """
    dir = os.path.dirname(sys.executable)
    file = os.path.basename(dir).lower() + ".dll"
    path = os.path.join(dir, file)
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError("Can't find python DLL...")


string = """
======================
  reapy config infos
======================

Python DLL
----------
    {}

Enable or disable reapy dist API
--------------------------------
Enable dist API
    {}

Disable dist API
    {}
"""

if __name__ == "__main__":
    try:
        dll = get_python_dll()
    except FileNotFoundError as e:
        dll = e.args[0]
    enable, disable = get_config_scripts()
    print(string.format(dll, enable, disable))
