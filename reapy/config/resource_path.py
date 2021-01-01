"""Find REAPER resource path without ``reapy`` dist API enabled."""

import os
import sys

import reapy
from .shared_library import is_windows, is_apple

if not reapy.is_inside_reaper():
    # Third-party imports crash REAPER when run inside it.
    import psutil


def get_candidate_directories(detect_portable_install=True):
    if detect_portable_install:
        yield get_portable_resource_directory()
    if is_apple():
        yield os.path.expanduser('~/Library/Application Support/REAPER')
    elif is_windows():
        yield os.path.expandvars(r'$APPDATA\REAPER')
    else:
        yield os.path.expanduser('~/.config/REAPER')


def get_portable_resource_directory():
    process_path = get_reaper_process_path()
    if is_apple():
        return '/'.join(process_path.split('/')[:-4])
    return os.path.dirname(process_path)


def get_reaper_process_path():
    """Return path to currently running REAPER process.

    Returns
    -------
    str
        Path to executable file.

    Raises
    ------
    RuntimeError
        When zero or more than one REAPER instances are currently
        running.
    """
    processes = [
        p for p in psutil.process_iter(['name', 'exe'])
        if os.path.splitext(p.info['name'])[0].lower() == 'reaper'
    ]
    if not processes:
        raise RuntimeError('No REAPER instance is currently running.')
    elif len(processes) > 1:
        raise RuntimeError(
            'More than one REAPER instance is currently running.'
        )
    return processes[0].info['exe']


def get_resource_path(detect_portable_install=True):
    for dir in get_candidate_directories(detect_portable_install):
        if os.path.exists(os.path.join(dir, 'reaper.ini')):
            return dir
