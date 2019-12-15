import reapy
import reapy.reascript_api as RPR
import contextlib
from .defer import ReaperConsole

import collections
import io
import os
import sys


_ORIGINAL_PRINT = print


def add_reascript(path, section_id=0, commit=True):
    """
    Add a ReaScript and return the new action ID.

    Parameters
    ----------
    path : str
        Path to script.
    section_id : int, optional (default=0, corresponds to main section).
        Action section ID to which the script must be added.
    commit : bool, optional
        Whether to commit change. Use it when adding a single script.
        You can optimize bulk adding `n` scripts by setting
        `commit=False` for the first `n-1` calls and `commit=True` for
        the last call.

    Returns
    -------
    action_id : int
        New ReaScript action ID.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    path = os.path.abspath(path)
    action_id = RPR.AddRemoveReaScript(
        True, section_id, path, commit
    )
    if action_id == 0:
        message = "Script at {} wasn't successfully added.".format(path)
        raise ValueError(message)
    return action_id


def arm_command(command_id, section=""):
    """
    Arm or disarm command.

    Parameters
    ----------
    command_id : int
        Command ID. If 0, disarm command.
    section : str, optional
        Command section. Empty string for main section. Default="".
    """
    RPR.ArmCommand(command_id, section)


def browse_for_file(window_title="", extension=""):
    """
    Ask the user to select a file.

    Parameters
    ----------
    window_title : str, optional
        Window title (default="")
    extension : str, optional
        Extension for file (e.g. "mp3", "txt"...) (default=all types).

    Returns
    -------
    path : str or NoneType
        Path to file, or None if user cancelled.
    """
    success, path, *_ = RPR.GetUserFileNameForRead("", window_title, extension)
    if success:
        return path


def clear_console():
    """
    Clear Reaper console.

    See also
    --------
    ReaProject.show_console_message
    """
    RPR.ClearConsole()


def clear_peak_cache():
    """
    Reset global peak cache.
    """
    RPR.ClearPeakCache()


def dB_to_slider(db):
    """
    Convert decibel value to slider.

    Parameters
    ----------
    db : float
        Decibel value.

    Returns
    -------
    slider : float
        Slider value.

    See also
    --------
    slider_to_dB
    """
    slider = RPR.DB2SLIDER(db)
    return slider


def delete_ext_state(section, key, persist=False):
    """
    Delete extended state value for a given section and key.

    Parameters
    ----------
    section : str
        Extended state section.
    key : str
        Extended state key.
    persist : bool
        Whether extended state should remain deleted next time REAPER
        is opened.
    """
    RPR.DeleteExtState(section, key, persist)


def disarm_command():
    """
    Disarm command.
    """
    arm_command(0)


def get_armed_command():
    command_id, section, _ = RPR.GetArmedCommand("", 2048)
    if command_id == 0:
        return
    return command_id, section


def get_command_id(command_name):
    """
    Return ID of command with a given name.

    Parameters
    ----------
    command_name : str
        Command name.

    Returns
    -------
    command_id : int or None
        Command ID, or None if name can't be found.
    """
    command_id = RPR.NamedCommandLookup(command_name)
    command_id = command_id if command_id else None
    return command_id


def get_command_name(command_id):
    """
    Return name of command with a given ID.

    Parameters
    ----------
    command_id : int
        Command ID.

    Returns
    -------
    command_name : str, None
        Command name, or None for a native command.
    """
    command_name = RPR.ReverseNamedCommandLookup(command_id)
    if command_name is not None:
        command_name = "_" + command_name
    return command_name


def get_exe_dir():
    """
    Return REAPER.exe directory (e.g. "C:\\Program Files\\REAPER").

    Returns
    -------
    path : str
        Path to REAPER.exe directory.
    """
    path = RPR.GetExePath()
    return path


def get_ext_state(section, key):
    """
    Get the extended state value for a specific section and key.

    Parameters
    ----------
    section : str
        Extended state section.
    key : str
        Extended state key for section `section`.

    Returns
    -------
    value : str
        Extended state value.

    See also
    --------
    delete_ext_state
    set_ext_state
    """
    value = RPR.GetExtState(section, key)
    return value


def get_global_automation_mode():
    """
    Return global automation override mode.

    Returns
    -------
    override_mode : str
        One of the following values:
            "bypass"
            "latch"
            "none"
            "read"
            "touch"
            "trim/read"
            "write"
    """
    modes = {
         -1: "none",
         0: "trim/read",
         1: "read",
         2: "touch",
         3: "write",
         4: "latch",
         5: "bypass"
    }
    override_mode = modes[RPR.GetGlobalAutomationOverride()]
    return override_mode


def get_ini_file():
    """
    Return path to REAPER.ini file.

    Returns
    -------
    path : str
        Path to REAPER.ini file.
    """
    path = RPR.get_ini_file()
    return path


def get_last_touched_track():
    """
    Return last touched track, or None if no track has been touched.

    Returns
    -------
    track : Track or None if no track has been touched.
    """
    track = reapy.Track(RPR.GetLastTouchedTrack())
    if not track._is_defined:
        track = None
    return track


def get_main_window():
    """
    Return main window.

    Returns
    -------
    window : Window
        Main window.
    """
    window = reapy.Window(RPR.GetMainHwnd())
    return window


@reapy.inside_reaper()
def get_projects():
    """
    Return list of all opened projects.

    Returns
    -------
    projects : list of Project
        List of all projects.
    """
    i, projects = 0, [reapy.Project(index=0)]
    while projects[-1]._is_defined:
        i += 1
        projects.append(reapy.Project(index=i))
    projects.pop()
    return projects


def get_reaper_version():
    version = RPR.GetAppVersion()
    return version


def get_resource_path():
    """
    Return path to directory where .ini files are stored.

    Returns
    -------
    path : str
        Path to directory where .ini files are stored.
    """
    path = RPR.GetResourcePath()
    return path


def has_ext_state(section, key):
    """
    Return whether extended state exists for given section and key.

    Parameters
    ----------
    section : str
        Extended state section.
    key : str
        Extended state key.

    Returns
    -------
    has_ext_state : bool
    """
    has_ext_state = bool(RPR.HasExtState(section, key))
    return has_ext_state


def open_project(filepath):
    """
    Open project and return it.

    Returns
    -------
    project : Project
        Opened project.
    """
    RPR.Main_openProject(filepath)
    project = reapy.Project()
    return project


def perform_action(action_id):
    """
    Perform action with ID `action_id` in the main Actions section.

    Parameters
    ----------
    action_id : int
        Action ID in the main Actions section.
    """
    RPR.Main_OnCommand(action_id, 0)


class prevent_ui_refresh(contextlib.ContextDecorator):
    """Class to prevent UI refresh on certain pieces of code.

    Its instance can be used both as decorator and as context manager:

    >>> with reapy.prevent_ui_refresh():
    ...     reapy.Project.add_track()

    >>> @prevent_ui_refresh()
    >>> def some_function(*args, **kwargs):
    ...     reapy.Project.add_track()

    """

    def __enter__(self):
        RPR.PreventUIRefresh(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        RPR.PreventUIRefresh(-1)


def print(*args, **kwargs):
    """
    Alias to ReaProject.show_console_message.
    """
    show_console_message(*args, **kwargs)


class reaprint(contextlib.ContextDecorator):
    """Class to send all prints to ReaperConsole.

    Its instance can be used both as decorator and context manager:

    >>> with reapy.reaprint():
    ...     print('This will go to the console!')
    ...     print('All these contexted will go to the console!')

    >>> @reapy.reaprint()
    >>> def some_function(*args, **kwargs):
    ...     print('This will go to the console!')
    ...     print('All these decorated prints will go to the console!')

    """
    _original_stdouts = collections.deque()

    def __enter__(self):
        self._original_stdouts.append(sys.stdout)
        sys.stdout = ReaperConsole()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdouts.pop()


def remove_reascript(path, section_id=0, commit=True):
    """
    Remove a ReaScript.

    Parameters
    ----------
    path : str
        Path to script.
    section_id : int, optional (default=0, corresponds to main section).
        Action section ID to which the script must be added.
    commit : bool, optional
        Whether to commit change. Use it when removing a single script.
        You can optimize bulk removing `n` scripts by setting
        `commit=False` for the first `n-1` calls and `commit=True` for
        the last call.
    """
    path = os.path.abspath(path)
    success = RPR.AddRemoveReaScript(
        False, section_id, path, commit
    )
    if not success:
        message = "Script at {} wasn't successfully added.".format(path)
        raise ValueError(message)


def rgb_from_native(native_color):
    """
    Extract RGB values from a native (OS-dependent) color.

    Parameters
    ----------
    native_color : int
        Native color.

    Returns
    -------
    r, g, b : (int, int, int)
        RGB values between 0 and 255.
    """
    _, r, g, b = RPR.ColorFromNative(native_color, 0, 0, 0)
    return r, g, b


def rgb_to_native(rgb):
    """
    Make a native (OS-dependent) color from RGB values.

    Parameters
    ----------
    rgb : (int, int, int)
        RGB triplet of integers between 0 and 255.

    Returns
    -------
    native_color : int
        Native color.
    """
    native_color = RPR.ColorToNative(*rgb)
    return native_color


def set_ext_state(section, key, value, persist=False):
    """
    Set the extended state value for a specific section and key.

    Parameters
    ----------
    section : str
        Extended state section.
    key : str
        Extended state key for section `section`.
    value : str
        Extended state value for section `section` and key `key`.
    persist : bool
        Whether the value should be stored and reloaded the next time
        REAPER is opened.

    See also
    --------
    delete_ext_state
    get_ext_state
    """
    RPR.SetExtState(section, key, value, persist)


def set_global_automation_mode(mode):
    """
    Set global automation mode.

    Parameters
    ----------
    mode : str
        One of the following values:
            "bypass"
            "latch"
            "none"
            "read"
            "touch"
            "trim/read"
            "write"
    """
    modes = {
         "none": -1,
         "trim/read": 0,
         "read": 1,
         "touch": 2,
         "write": 3,
         "latch": 4,
         "bypass": 5
    }
    RPR.SetGlobalAutomationOverride(modes[mode])


def show_console_message(*args, sep=" ", end="\n"):
    """
    Print a message to the Reaper console.

    Parameters
    ----------
    args : tuple
        Values to print.
    sep : str, optional
        String inserted between values (default=" ").
    end : str, optional
        String appended after the last value (default="\n").
    """
    file = io.StringIO()
    _ORIGINAL_PRINT(*args, sep=sep, end=end, file=file)
    file.seek(0)
    txt = file.read()
    RPR.ShowConsoleMsg(txt)


def show_message_box(text="", title="", type="ok"):
    """
    Show message box.

    Parameters
    ----------
    text : str
        Box message
    title : str
        Box title
    type : str
        One of the following values.

        "ok"
        "ok-cancel"
        "abort-retry-ignore"
        "yes-no-cancel"
        "yes-no"
        "retry-cancel"

    Returns
    -------
    status : str
        One of the following values.

        "ok"
        "cancel"
        "abort"
        "retry"
        "ignore"
        "yes"
        "no"
    """
    all_types = {
        "ok": 0,
        "ok-cancel": 1,
        "abort-retry-ignore": 2,
        "yes-no-cancel": 3,
        "yes-no": 4,
        "retry-cancel": 5
    }
    all_status = {
        1: "ok",
        2: "cancel",
        3: "abort",
        4: "retry",
        5: "ignore",
        6: "yes",
        7: "no"
    }
    status = RPR.ShowMessageBox(text, title, all_types[type])
    status = all_status[status]
    return status


def slider_to_dB(slider):
    """
    Convert slider value to decibel.

    Parameters
    ----------
    slider : float
        Slider value.

    Returns
    -------
    db : float
        Decibel value.

    See also
    --------
    dB_to_slider
    """
    db = RPR.SLIDER2DB(slider)
    return db


def test_api():
    """Display a message window if the API can successfully be called."""
    RPR.APITest()


class undo_block(contextlib.ContextDecorator):
    """Class to register undo block.

    Its instance can be used both as decorator and context manager:

    >>> with reapy.undo_block('add track'):
    ...     reapy.Project.add_track()

    >>> @reapy.undo_block('add track')
    >>> def some_function(*args, **kwargs):
    ...     reapy.Project.add_track()

    :param undo_name: Str to register undo name (shown later in Undo menu)
    :param flags: Int to pass to Undo_EndBlock
                    (leave default if you don't know what it is)
    """

    def __init__(self, undo_name, flags=0):
        self.undo_name = undo_name
        self.flags = flags

    def __enter__(self):
        RPR.Undo_BeginBlock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        RPR.Undo_EndBlock(self.undo_name, self.flags)


def update_arrange():
    """
    Redraw the arrange view.
    """
    RPR.UpdateArrange()


def update_timeline():
    """
    Redraw the arrange view and ruler.
    """
    RPR.UpdateTimeline()


def view_prefs():
    """
    Open Preferences.
    """
    RPR.ViewPrefs(0, "")
