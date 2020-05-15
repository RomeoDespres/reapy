import os
import sys

from .shared_library import is_windows, is_apple


def get_windows_candidates():
    # Normal installation
    yield os.path.join(os.path.expandvars('$APPDATA'), 'REAPER')
    # Default path for portable installations
    yield os.path.abspath(r'\REAPER')
