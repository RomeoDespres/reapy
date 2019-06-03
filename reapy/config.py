import reapy
from reapy.errors import OutsideREAPERError
from reapy.reascripts import activate_reapy_server

from configparser import ConfigParser
from collections import OrderedDict
import json
import os

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

    def __init__(self):
        super(Config, self).__init__(strict=False, delimiters="=", dict_type=CaseInsensitiveDict)
        self.optionxform = str
        ini_filename = reapy.get_ini_file()
        self.read(ini_filename, encoding='utf8')

    def write(self):
        ini_filename = reapy.get_ini_file()
        with open(ini_filename, encoding='utf8') as f_old:
            old_config_content = f_old.read()

        # this is to save first config which user had before trying reapy
        ini_before_reapy_filename = ini_filename + '.before-reapy.bak'
        if not os.path.exists(ini_before_reapy_filename):
            with open(ini_before_reapy_filename, 'w', encoding='utf8') as f:
                f.write(old_config_content)

        # this is current ini file backup copy
        ini_bak_filename = ini_filename + '.bak'
        with open(ini_bak_filename, 'w', encoding='utf8') as f:
            f.write(old_config_content)

        # write to tmp file first
        tmp_filename = ini_filename + '.tmp'
        with open(tmp_filename, "w", encoding='utf8') as f:
            super(Config, self).write(f, False)

        # then rename tmp to ini file
        os.replace(tmp_filename, ini_filename)


def create_new_web_interface(port):
    """
    Create a Web interface in REAPER at a specified port.

    It is added by writing a line directly in REAPER .ini file. Thus
    it will only be available on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    config = Config()
    csurf_count = int(config["reaper"].get("csurf_cnt", "0"))
    csurf_count += 1
    config["reaper"]["csurf_cnt"] = str(csurf_count)
    key = "csurf_{}".format(csurf_count - 1)
    config["reaper"][key] = "HTTP 0 {} '' 'index.html' 0 ''".format(port)
    config.write()


def delete_web_interface(port):
    """
    Delete Web interface listening to a specified port.

    It is deleted by writing a line directly in REAPER .ini file. Thus
    it will only be deleted on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    config = Config()
    # Get number of enabled control surfaces
    csurf_count = int(config["reaper"]["csurf_cnt"])
    # Find the one describing the web interface
    for i in range(csurf_count):
        string = config["reaper"]["csurf_{}".format(i)]
        if string.startswith("HTTP"):  # It's a web interface
            if string.split(" ")[2] == str(port):  # It's the one
                webi_index = i
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
    delete_web_interface(WEB_INTERFACE_PORT)
    reascript_path = get_activate_reapy_server_path()
    reapy.remove_reascript(reascript_path)
    message = (
        "reapy will be disabled as soon as you restart REAPER."
    )
    reapy.show_message_box(message)


def enable_dist_api():
    """
    Enable distant API.

    Create a Web interface and add the ReaScript
    ``reapy.reascripts.activate_reapy_server`` to the Actions list.
    """
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


def get_activate_reapy_server_path():
    """Return path to the ``activate_reapy_server`` ReaScript."""
    return os.path.abspath(activate_reapy_server.__file__)
