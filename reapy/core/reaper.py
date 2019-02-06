from reapy import reascript_api as RPR

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
