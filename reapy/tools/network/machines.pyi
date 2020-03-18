import importlib
import sys
import warnings
import typing as ty
from builtins import BaseException
from types import TracebackType

import reapy
import reapy.config
from reapy import errors
from . import client, web_interface


CLIENT: ty.Optional[client.Client]
CLIENTS: ty.Dict[ty.Optional[str], ty.Optional[client.Client]]


def get_selected_client() -> ty.Optional[client.Client]:
    ...


def get_selected_machine_host() -> ty.Optional[str]:
    """Return host of the currently selected machine.

    Returns
    -------
    host : str or None
        None is returned when running from inside REAPER and
        no slave machine is selected.
    """
    ...


def reconnect() -> None:
    """
    Reconnect to REAPER ReaScript API.

    Examples
    --------
    Assume no REAPER instance is active.
    >>> import reapy
    errors.DisabledDistAPIWarning: Can't reach distant API. Please start REAPER, or
    call reapy.config.enable_dist_api() from inside REAPER to enable distant
    API.
      warnings.warn(errors.DisabledDistAPIWarning())
    >>> p = reapy.Project()  # Results in error
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "reapy\\core\\project\\project.py", line 26, in __init__
        id = RPR.EnumProjects(index, None, 0)[0]
    AttributeError: module 'reapy.reascript_api' has no attribute 'EnumProjects'
    >>> # Now start REAPER
    ...
    >>> reapy.reconnect()
    >>> p = reapy.Project()  # No error!
    """
    ...


class connect:

    """Connect to slave machine.

    reapy instructions will now be run on the selected machine.
    If used as a context manager, the slave machine will only be
    selected in the corresponding context.

    Parameters
    ----------
    host : str, optional
        Slave machine host. If None, selects default ``reapy``
        behavior (i.e. local REAPER instance).

    See also
    --------
    ``connect_to_default_machine``
        Connect to default slave machine (i.e. local REAPER instance).
    """

    previous_client: ty.Optional[client.Client]

    def __init__(self, host: ty.Optional[str] = None) -> None:
        ...

    def __enter__(self) -> 'connect':
        ...

    def __exit__(self,
                 type: ty.Optional[ty.Type[BaseException]],
                 value: ty.Optional[BaseException],
                 traceback: ty.Optional[TracebackType]) -> None:
        ...


class connect_to_default_machine(connect):

    """Select default slave machine (i.e. local REAPER instance)."""

    def __init__(self) -> None:
        ...


def register_machine(host: str) -> None:
    """Register a slave machine.

    Parameters
    ----------
    host : str
        Slave machine host (e.g. ``"localhost"``).

    See also
    --------
    ``reapy.connect``
    """
    ...
