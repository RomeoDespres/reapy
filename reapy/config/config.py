from configparser import ConfigParser
from collections import OrderedDict
import json
import os
import pathlib
import random
import re
import shutil
import string
import warnings

import reapy
from reapy.errors import OutsideREAPERError
from reapy.reascripts import activate_reapy_server
from .resource_path import get_resource_path
from .shared_library import get_python_shared_library


__all__ = [
    'add_web_interface',
    'configure_reaper',
    'create_new_web_interface',
    'delete_web_interface',
    'disable_dist_api',
    'enable_dist_api',
    'enable_python',
    'REAPY_SERVER_PORT',
    'WEB_INTERFACE_PORT'
]


REAPY_SERVER_PORT = 2306
WEB_INTERFACE_PORT = 2307


class CaseInsensitiveDict(OrderedDict):

    """OrderedDict with case-insensitive keys."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = OrderedDict(*args, **kwargs)
        for key, value in self._dict.items():
            self._dict[key.lower()] = value

    def __contains__(self, key):
        return key.lower() in self._dict

    def __getitem__(self, key):
        return self._dict[key.lower()]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._dict[key.lower()] = value


class Config(ConfigParser):

    """Parser for REAPER .ini file."""

    def __init__(self, ini_file):
        super().__init__(
            strict=False, delimiters="=", dict_type=CaseInsensitiveDict
        )
        self.optionxform = str
        self.ini_file = ini_file
        if not os.path.exists(ini_file):
            pathlib.Path(ini_file).touch()
        self.read(self.ini_file, encoding='utf8')

    def write(self):
        # Backup config state before user has ever tried reapy
        before_reapy_file = self.ini_file + '.before-reapy.bak'
        if not os.path.exists(before_reapy_file):
            shutil.copy(self.ini_file, before_reapy_file)
        # Backup current config
        shutil.copy(self.ini_file, self.ini_file + '.bak')
        # Write config
        with open(self.ini_file, "w", encoding='utf8') as f:
            super().write(f, False)


def add_reascript(resource_path, script_path):
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
    script_path = os.path.abspath(script_path)
    if not os.path.exists(script_path):
        raise FileNotFoundError(script_path)
    if os.path.splitext(script_path)[1] != '.py':
        raise ValueError('{} is not a Python module.'.format(script_path))
    ini_file = os.path.join(resource_path, "reaper-kb.ini")
    if not os.path.exists(ini_file):
        pathlib.Path(ini_file).touch()
    # Check if ReaScript already exists
    with open(ini_file) as f:
        lines = re.findall("^SCR 4 0 .*", f.read(), re.MULTILINE)
    for line in lines:
        if line.split(" ")[-1] == script_path:
            return '"_{}"'.format(line.split(" ")[3].strip('_'))
    # If not, add it
    code = get_new_reascript_code(ini_file)
    script_name = os.path.basename(script_path)
    new_line = 'SCR 4 0 {} "Custom: {}" {}'
    with open(ini_file, "a") as f:
        f.write(new_line.format(code, script_name, script_path))
    return '"_{}"'.format(code)


def add_web_interface(resource_path, port=WEB_INTERFACE_PORT):
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
    if web_interface_exists(resource_path, port):
        return
    config = Config(os.path.join(resource_path, "reaper.ini"))
    csurf_count = int(config["reaper"].get("csurf_cnt", "0"))
    csurf_count += 1
    config["reaper"]["csurf_cnt"] = str(csurf_count)
    key = "csurf_{}".format(csurf_count - 1)
    config["reaper"][key] = "HTTP 0 {} '' 'index.html' 0 ''".format(port)
    config.write()


def configure_reaper(resource_path=None, detect_portable_install=True):
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
    if resource_path is None:
        resource_path = get_resource_path(detect_portable_install)
    enable_python(resource_path)
    add_web_interface(resource_path)
    action = add_reascript(resource_path, get_activate_reapy_server_path())
    set_ext_state("reapy", "activate_reapy_server", action, resource_path)


def create_new_web_interface(port):
    """Create a Web interface in REAPER at a specified port.

    .. deprecated:: 0.8.0
          ``create_new_web_interface`` will be removed in reapy 1.0.0.
          Use :func:`reapy.config.add_web_interface` that works from
          outside REAPER.

    It is added by writing a line directly in REAPER .ini file. Thus
    it will only be available on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    msg = (
        "Function create_new_web_interface is deprecated since 0.8.0. "
        "Use reapy.config.add_web_interface instead."
    )
    warnings.warn(FutureWarning(msg))
    config = Config(reapy.get_ini_file())
    csurf_count = int(config["reaper"].get("csurf_cnt", "0"))
    csurf_count += 1
    config["reaper"]["csurf_cnt"] = str(csurf_count)
    key = "csurf_{}".format(csurf_count - 1)
    config["reaper"][key] = "HTTP 0 {} '' 'index.html' 0 ''".format(port)
    config.write()


def delete_web_interface(resource_path, port=WEB_INTERFACE_PORT):
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
    config = Config(os.path.join(resource_path, "reaper.ini"))
    # Get number of enabled control surfaces
    csurf_count = int(config["reaper"]["csurf_cnt"])
    # Find the one describing the web interface
    for i in range(csurf_count):
        string = config["reaper"]["csurf_{}".format(i)]
        if string.startswith("HTTP"):  # It's a web interface
            if string.split(" ")[2] == str(port):  # It's the one
                webi_index = i
    if 'webi_index' in locals():  # Means we found it
        # Remove the line...
        del config["reaper"]["csurf_{}".format(webi_index)]
        # ...and move the following lines one step above
        for i in range(webi_index, csurf_count - 1):
            next_line = config["reaper"]["csurf_{}".format(i + 1)]
            config["reaper"]["csurf_{}".format(i)] = next_line
        # Update number of control surfaces
        config["reaper"]["csurf_cnt"] = str(csurf_count - 1)
        # And write it out
        config.write()


def disable_dist_api():
    """
    Disable distant API.

    Delete ``reapy`` Web interface, and remove the ReaScript
    ``reapy.reascripts.activate_reapy_server`` from the
    Actions list.
    """
    if not reapy.is_inside_reaper():
        raise OutsideREAPERError
    delete_web_interface(reapy.get_resource_path(), WEB_INTERFACE_PORT)
    reascript_path = get_activate_reapy_server_path()
    reapy.remove_reascript(reascript_path)
    message = (
        "reapy will be disabled as soon as you restart REAPER."
    )
    reapy.show_message_box(message)


def enable_dist_api():
    """Enable distant API.

    .. deprecated:: 0.8.0
          ``enable_dist_api`` will be removed in reapy 1.0.0.
          Use :func:`reapy.config.configure_reaper` that works
          even from outside REAPER.

    Create a Web interface and add the ReaScript
    ``reapy.reascripts.activate_reapy_server`` to the Actions list.
    """
    msg = (
        "Function enable_dist_api is deprecated since 0.8.0. "
        "Use reapy.config.configure_reaper instead."
    )
    warnings.warn(FutureWarning(msg))
    if not reapy.is_inside_reaper():
        raise OutsideREAPERError
    create_new_web_interface(WEB_INTERFACE_PORT)
    reascript_path = get_activate_reapy_server_path()
    action_id = reapy.add_reascript(reascript_path)
    command_name = json.dumps(reapy.get_command_name(action_id))
    section, key, value = "reapy", "activate_reapy_server", command_name
    reapy.set_ext_state(section, key, value, persist=True)
    message = (
        "reapy successfully enabled!\n\nPlease restart REAPER.\n\nYou will "
        "then be able to import reapy from the outside."
    )
    reapy.show_message_box(message)


def enable_python(resource_path):
    shared_library = get_python_shared_library()
    config = Config(os.path.join(resource_path, "reaper.ini"))
    config["reaper"]["reascript"] = "1"
    config["reaper"]["pythonlibpath64"] = os.path.dirname(shared_library)
    config["reaper"]["pythonlibdll64"] = os.path.basename(shared_library)
    config.write()


def get_activate_reapy_server_path():
    """Return path to the ``activate_reapy_server`` ReaScript."""
    script_path = os.path.abspath(activate_reapy_server.__file__)
    if script_path.endswith(('.pyc', '.pyw')):
        script_path = script_path[:-1]
    return script_path


def get_new_reascript_code(ini_file):
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
    def get_random_code():
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(40))
    with open(ini_file) as f:
        content = f.read()
    code = get_random_code()
    while code in content:
        code = get_random_code()
    return "RS" + code


def set_ext_state(section, key, value, resource_path):
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
    config = Config(os.path.join(resource_path, 'reaper-extstate.ini'))
    if section not in config.sections():
        config.add_section(section)
    config[section][key] = value
    config.write()


def web_interface_exists(resource_path, port=WEB_INTERFACE_PORT):
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
    config = Config(os.path.join(resource_path, "reaper.ini"))
    csurf_count = int(config["reaper"].get("csurf_cnt", "0"))
    for i in range(csurf_count):
        string = config["reaper"]["csurf_{}".format(i)]
        if string.startswith("HTTP"):  # It's a web interface
            if string.split(" ")[2] == str(port):  # It's the one
                return True
    return False
