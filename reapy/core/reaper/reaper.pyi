import reapy
import reapy.reascript_api as RPR
import contextlib
from .defer import ReaperConsole

import collections
import io
import os
import sys
import typing as ty

_ORIGINAL_PRINT = print


def add_reascript(path: str, section_id: int = 0, commit: bool = True) -> int:
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
    ...


def arm_command(command_id: int, section: str = "") -> None:
    """
    Arm or disarm command.

    Parameters
    ----------
    command_id : int
        Command ID. If 0, disarm command.
    section : str, optional
        Command section. Empty string for main section. Default="".
    """
    ...


def browse_for_file(window_title: str = "",
                    extension: str = "") -> ty.Optional[str]:
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
    ...


def clear_console() -> None:
    """
    Clear Reaper console.

    See also
    --------
    ReaProject.show_console_message
    """
    ...


def clear_peak_cache() -> None:
    """
    Reset global peak cache.
    """
    ...


def dB_to_slider(db: float) -> float:
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
    ...


def delete_ext_state(section: str, key: str, persist: bool = False) -> None:
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
    ...


def disarm_command() -> None:
    """
    Disarm command.
    """
    ...


def get_armed_command() -> ty.Optional[ty.Tuple[int, str]]:
    ...


def get_command_id(command_name: str) -> ty.Optional[int]:
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
    ...


def get_command_name(command_id: int) -> ty.Optional[str]:
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
    ...


def get_exe_dir() -> str:
    """
    Return REAPER.exe directory (e.g. "C:\\Program Files\\REAPER").

    Returns
    -------
    path : str
        Path to REAPER.exe directory.
    """
    ...


def get_ext_state(section: str, key: str) -> str:
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
    ...


def get_global_automation_mode() -> str:
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
    ...


def get_ini_file() -> str:
    """
    Return path to REAPER.ini file.

    Returns
    -------
    path : str
        Path to REAPER.ini file.
    """
    ...


def get_last_touched_track() -> ty.Optional[reapy.Track]:
    """
    Return last touched track, or None if no track has been touched.

    Returns
    -------
    track : Track or None if no track has been touched.
    """
    ...


def get_main_window() -> reapy.Window:
    """
    Return main window.

    Returns
    -------
    window : Window
        Main window.
    """
    ...


@reapy.inside_reaper()
def get_projects() -> ty.List[reapy.Project]:
    """
    Return list of all opened projects.

    Returns
    -------
    projects : list of Project
        List of all projects.
    """
    ...


def get_reaper_version() -> str:
    ...


def get_resource_path() -> str:
    """
    Return path to directory where .ini files are stored.

    Returns
    -------
    path : str
        Path to directory where .ini files are stored.
    """
    ...


def has_ext_state(self, section: str, key: str) -> bool:
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
    ...


def open_project(filepath: str) -> reapy.Project:
    """
    Open project and return it.

    Returns
    -------
    project : Project
        Opened project.
    """
    ...


def perform_action(action_id: int) -> None:
    """
    Perform action with ID `action_id` in the main Actions section.

    Parameters
    ----------
    action_id : int
        Action ID in the main Actions section.
    """
    ...


class prevent_ui_refresh(contextlib.ContextDecorator):
    """Class to prevent UI refresh on certain pieces of code.

    Its instance can be used both as decorator and as context manager:

    >>> with reapy.prevent_ui_refresh():
    ...     reapy.Project.add_track()

    >>> @prevent_ui_refresh()
    >>> def some_function(*args, **kwargs):
    ...     reapy.Project.add_track()

    """
    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type: Exception, exc_val: ty.Any,
                 exc_tb: ty.Any) -> None:
        ...


def print(*args: ty.Any, **kwargs: ty.Any) -> None:
    """
    Alias to ReaProject.show_console_message.
    """
    ...


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
    _original_stdouts: ty.Deque[str]

    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type: ty.Any, exc_val: ty.Any,
                 exc_tb: ty.Any) -> None:
        ...


def remove_reascript(path: str, section_id: int = 0,
                     commit: bool = True) -> None:
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
    ...


def rgb_from_native(native_color: int) -> ty.Tuple[int, int, int]:
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
    ...


def rgb_to_native(rgb: ty.Tuple[int, int, int]) -> int:
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
    ...


def set_ext_state(section: int, key: str, value: str,
                  persist: bool = False) -> None:
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
    ...


def set_global_automation_mode(mode: str) -> None:
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
    ...


def show_console_message(*args: ty.Any, sep: str = " ",
                         end: str = "\n") -> None:
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
    ...


def show_message_box(text: str = "", title: str = "", type: str = "ok") -> str:
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
    ...


def slider_to_dB(slider: float) -> float:
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
    ...


def test_api() -> None:
    """Display a message window if the API can successfully be called."""
    ...


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
    undo_name: str
    flags: int

    def __init__(self, undo_name: str, flags: int = 0):
        ...

    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type: ty.Any, exc_val: ty.Any,
                 exc_tb: ty.Any) -> None:
        ...


def update_arrange() -> None:
    """
    Redraw the arrange view.
    """
    ...


def update_timeline() -> None:
    """
    Redraw the arrange view and ruler.
    """
    ...


def view_prefs() -> None:
    """
    Open Preferences.
    """
    ...
