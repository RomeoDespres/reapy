import importlib
import sys
import warnings

import reapy
import reapy.config
from reapy import errors
from . import client, web_interface


CLIENT = None
CLIENTS = {None: None}


def get_selected_client():
    return CLIENT


def get_selected_machine_host():
    """Return host of the currently selected machine.

    Returns
    -------
    host : str or None
        None is returned when running from inside REAPER and
        no slave machine is selected.
    """
    return None if CLIENT is None else CLIENT.host


def reconnect():
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
    if not reapy.is_inside_reaper():
        host = get_selected_machine_host()
        if host is None:
            # We are outside REAPER, so this means initial import failed to
            # connect and we want to retry with default host (i.e. localhost)
            host = "localhost"
        try:
            del CLIENTS[host]
        except KeyError:
            pass
        connect(host)


def is_connected():
    """
    Get connection state of reapy.

    Returns
    -------
    Union[str, bool]
        if connected — returns host as str (localhost also can be returned)
        if not — returns False
    """
    global CLIENT
    if CLIENT is None:
        return False
    return CLIENT.host


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

    def __init__(self, host=None):
        global CLIENT
        self.previous_client = CLIENT
        try:
            if host not in CLIENTS:
                register_machine(host)
            CLIENT = CLIENTS[host]
            if hasattr(reapy, 'reascript_api'):  # False during initial import
                importlib.reload(reapy.reascript_api)
        except errors.DisabledDistAPIError as e:
            if host and host != 'localhost':
                raise e
            warnings.warn(errors.DisabledDistAPIWarning())

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        global CLIENT
        CLIENT = self.previous_client
        importlib.reload(reapy.reascript_api)


class connect_to_default_machine(connect):

    """Select default slave machine (i.e. local REAPER instance)."""

    def __init__(self):
        super().__init__()


def register_machine(host):
    """Register a slave machine.

    Parameters
    ----------
    host : str
        Slave machine host (e.g. ``"localhost"``).

    See also
    --------
    ``reapy.connect``
    """
    if reapy.is_inside_reaper() and host == "localhost":
        msg = "A REAPER instance can not connect to istelf."
        raise errors.InsideREAPERError(msg)
    interface_port = reapy.config.WEB_INTERFACE_PORT
    interface = web_interface.WebInterface(interface_port, host)
    CLIENTS[host] = client.Client(interface.get_reapy_server_port(), host)


if not reapy.is_inside_reaper():
    connect("localhost")
    CLIENTS[None] = CLIENT
