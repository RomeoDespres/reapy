"""Get setup infos."""

import os, sys


def get_config_scripts():
    dir = os.path.dirname(__file__)
    return (
        os.path.join(dir, "config", "enable_dist_api.py"),
        os.path.join(dir, "config", "disable_dist_api.py")
    )
    
def get_python_dll():
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