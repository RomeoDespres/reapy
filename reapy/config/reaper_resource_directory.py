import os
import sys

from .shared_library import is_windows, is_apple


def get_apple_candidates():
    yield os.path.expanduser(
        os.path.join('~', 'Library', 'Application Support', 'REAPER')
    )


def get_windows_candidates():
    # Normal installation
    yield os.path.expandvars(os.path.join('$APPDATA', 'REAPER'))
    # Default path for portable installations
    yield os.path.abspath(r'\REAPER')
