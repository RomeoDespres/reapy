from reapy import reascript_api as RPR

import io, os

_original_print = print

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
    action_id = RPR.AddRemoveReaScript(
        True, section_id, path, commit
    )
    if action_id == 0:
        raise ValueError("Script at {} wasn't successfully added.".format(path))
    return action_id
    
def clear_console():
    """
    Clear Reaper console.

    See also
    --------
    ReaProject.show_console_message
    """
    RPR.ClearConsole()

def get_exe_dir():
    """
    Return REAPER.exe directory (e.g. "C:\Program Files\REAPER").
    
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
    """
    value = RPR.GetExtState(section, key)
    return value
    
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
    
def perform_action(action_id):
    """
    Perform action with ID `action_id` in the main Actions section.

    Parameters
    ----------
    action_id : int
        Action ID in the main Actions section.
    """
    RPR.Main_OnCommand(action_id, 0)
    
def print(*args, **kwargs):
    """
    Alias to ReaProject.show_console_message.
    """
    show_console_message(*args, **kwargs)
    
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
    success = RPR.AddRemoveReaScript(
        False, section_id, path, commit
    )
    if not success:
        raise ValueError("Script at {} wasn't successfully added.".format(path))
    
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
    """
    RPR.SetExtState(section, key, value, persist)
    
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

    See also
    --------
    ReaProject.clear_console
    """
    file = io.StringIO()
    _original_print(*args, sep=sep, end=end, file=file)
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