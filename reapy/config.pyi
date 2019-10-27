import reapy
from reapy.errors import OutsideREAPERError
from reapy.reascripts import activate_reapy_server

from configparser import ConfigParser
from collections import OrderedDict
import json
import os
import shutil

import typing as ty

REAPY_SERVER_PORT = 2306
WEB_INTERFACE_PORT = 2307

T1 = ty.TypeVar('T1')
T2 = ty.TypeVar('T2')


class CaseInsensitiveDict(OrderedDict[str, T1]):
    """OrderedDict with case-insensitive keys."""
    _dict: OrderedDict[str, T1]

    def __init__(self, *args: T1, **kwargs: T1) -> None:
        ...

    def __contains__(self, key: str) -> ty.Union[str, bool]:  # type: ignore
        ...

    def __getitem__(self, key: str) -> T1:
        ...

    def __setitem__(self, key: str, value: T1) -> None:
        ...


class Config(ConfigParser):
    """Parser for REAPER .ini file."""
    ini_file: str

    def __init__(self) -> None:
        ...

    def write(self) -> None:
        # Backup config state before user has ever tried reapy
        ...


def create_new_web_interface(port: int) -> None:
    """
    Create a Web interface in REAPER at a specified port.

    It is added by writing a line directly in REAPER .ini file. Thus
    it will only be available on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    ...


def delete_web_interface(port: int) -> None:
    """
    Delete Web interface listening to a specified port.

    It is deleted by writing a line directly in REAPER .ini file. Thus
    it will only be deleted on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    ...


def disable_dist_api() -> None:
    """
    Disable distant API.

    Delete ``reapy`` Web interface, and remove the ReaScript
    ``reapy.reascripts.activate_reapy_server`` from the
    Actions list.
    """
    ...


def enable_dist_api() -> None:
    """
    Enable distant API.

    Create a Web interface and add the ReaScript
    ``reapy.reascripts.activate_reapy_server`` to the Actions list.
    """
    ...


def get_activate_reapy_server_path() -> str:
    """Return path to the ``activate_reapy_server`` ReaScript."""
    ...
