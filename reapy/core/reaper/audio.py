"""Audio handling functions."""

from reapy import reascript_api as RPR

def init():
    """
    Open all audio and MIDI devices (if not opened).
    """
    RPR.Audio_Init()
    
def is_prebuffer():
    """
    Return whether audio is in pre-buffer (threadsafe).
    
    Returns
    -------
    is_prebuffer : bool
        Whether audio is in pre-buffer.
    """
    is_prebuffer = bool(RPR.Audio_IsPreBuffer())
    return is_prebuffer
    
def is_running():
    """
    Return whether audio is running (threadsafe).
    
    Returns
    -------
    is_running : bool
        Whether audio is running.
    """
    is_running = bool(RPR.Audio_IsRunning())
    return is_running
    
def quit():
    """
    Close all audio and MIDI devices (if opened).
    """
    RPR.Audio_Quit()