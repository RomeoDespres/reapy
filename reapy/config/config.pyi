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

__all__ = [
    'add_web_interface',
    'configure_reaper',
    'create_new_web_interface',
    'delete_web_interface',
    'disable_dist_api',
    'enable_dist_api',
    'enable_python',
    'REAPY_SERVER_PORT',
    'WEB_INTERFACE_PORT',
]


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

    def write(self) -> None:  # type:ignore
        # Backup config state before user has ever tried reapy
        ...


def add_reascript(resource_path: str, script_path: str) -> str:
    """Add ReaScript to *Actions* list in REAPER.

    Works by manually editing ``reaper-kb.ini`` configuration file.
    Only use this function at setup time to configure REAPER.
    In other cases, make use of :func:`reapy.add_reascript`.

    In case ``script_path`` is already in Actions list, its command
    name is returned but it is not added a second time.

    Parameters
    ----------
    resource_path : str
        Path to REAPER resource directory. Can be obtained with
        :func:`reapy.config.resource_path.get_resource_path`.
    script_path : str
        Path to script that will be added.

    Returns
    -------
    str
        Action name for the newly added ReaScript.

    Raises
    ------
    FileNotFoundError
        When ``script_path`` does not exist.
    ValueError
        When ``script_path`` is not a Python module.
    """
    ...


def add_web_interface(
    resource_path: str, port: int = WEB_INTERFACE_PORT
) -> None:
    """Add a REAPER Web Interface at a specified port.

    It is added by manually editing reaper.ini configuration file,
    which is loaded on startup. Thus, the added web interface will
    only be available after restarting REAPER.

    Nothing happens in case a web interface already exists at
    ``port``.

    Parameters
    ----------
    resource_path : str
        Path to REAPER resource directory. Can be obtained with
        :func:`reapy.config.resource_path.get_resource_path`.
    port : int, optional
        Web interface port. Default=``2307``.
    """


def configure_reaper(
    resource_path: ty.Optional[str] = None,
    detect_portable_install: bool = True
) -> None:
    """Configure REAPER to allow reapy connections.

    Allows to use reapy from outside REAPER.

    Configuration is done by manually editing ``reaper.ini``
    and ``reaper-kb.ini``. It consists in the following steps:
    1. Enable usage of Python for ReaScripts.
    2. Fill in path to python shared library (.dll, .dylib or .so).
    3. Add a web interface on port 2307 to listen to reapy
       connections.
    4. Add the ReaScript ``reapy.reascripts.activate_reapy_server``
       to the *Actions* list.
    5. Add the name of this action to REAPER external state.

    It is safe to call this function several times as it only edits
    configuration files when needed.

    Parameters
    ----------
    resource_path : str or None, optional
        Path to REAPER resource directory. When ``None``, defaults to
        the result of
        :func:`reapy.config.resource_path.get_resource_path`. Use it
        if you already know where REAPER resource directory is
        located at.
    detect_portable_install : bool, optional
        If ``True``, this function will look for a currently running
        REAPER process and detect whether it is a portable install.
        If ``False``, configuration files will be looked for in the
        default locations only, which may result in a
        ``FileNotFoundError`` if no global REAPER install exists.
        Default=``True``.

    Raises
    ------
    RuntimeError
        When ``detect_portable_install=True`` and zero or more than one
        REAPER instances are currently running.
    FileNotFoundError
        When ``detect_portable_install=False`` but no global
        configuration file can be found (which means REAPER has only
        been installed as portable.)
    """
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


def delete_web_interface(
    resource_path: str, port: int = WEB_INTERFACE_PORT
) -> None:
    """Delete a REAPER Web Interface at a specified port.

    It is deleted by manually editing reaper.ini configuration file,
    which is loaded on startup. Thus, the web interface stay alive
    until REAPER is closed.

    Parameters
    ----------
    resource_path : str
        Path to REAPER resource directory. Can be obtained with
        :func:`reapy.config.resource_path.get_resource_path`.
    port : int, optional
        Web interface port. Default=``2307``.
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


def enable_python(resource_path: str) -> None:
    ...


def get_activate_reapy_server_path() -> str:
    """Return path to the ``activate_reapy_server`` ReaScript."""
    ...


def get_new_reascript_code(ini_file: str) -> str:
    """Return new ReaScript code for reaper-kb.ini.

    Parameters
    ----------
    ini_file : str
        Path to ``reaper-kb.ini`` configuration file.

    Returns
    -------
    code : str
        ReaScript code.
    """
    ...


def set_ext_state(
    section: str, key: str, value: str, resource_path: str
) -> str:
    """Update REAPER external state.

    Works by manually editing ``reaper-extstate.ini`` configuration file.
    Only use this function at setup time to configure REAPER.
    In other cases, make use of :func:`reapy.set_ext_state`.

    Parameters
    ----------
    section : str
        External state section.
    key : str
        External state key in ``section``.
    value : str
        External state value for ``key`` in ``section``.
    resource_path : str
        Path to REAPER resource directory. Can be obtained with
        :func:`reapy.config.resource_path.get_resource_path`.

    Returns
    -------
    str
        Action name for the newly added ReaScript.
    """
    ...


def web_interface_exists(
    resource_path: str, port: int = WEB_INTERFACE_PORT
) -> bool:
    """Return whether a REAPER Web Interface exists at a given port.

    Parameters
    ----------
    resource_path : str
        Path to REAPER resource directory. Can be obtained with
        :func:`reapy.config.resource_path.get_resource_path`.
    port : int, optional
        Web interface port. Default=``2307``.

    Returns
    -------
    bool
        Whether a REAPER Web Interface exists at ``port``.
    """
    ...
