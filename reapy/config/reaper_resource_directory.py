import os
import sys

from .shared_library import is_windows, is_apple


def get_apple_candidates():
    # Normal installation
    yield os.path.expanduser('~/Library/Application Support/REAPER')


def get_linux_candidates():
    # Default path for portable installation
    yield os.path.expanduser('~/.config/REAPER')
    # Default path for all-users full installation
    yield '/opt/REAPER'
    # Default path for current user only full installation
    yield os.path.expanduser('~/opt/REAPER')


def get_windows_candidates():
    # Normal installation
    yield os.path.expandvars(r'$APPDATA\REAPER'))
    # Default path for portable installation
    yield os.path.abspath(r'\REAPER')

