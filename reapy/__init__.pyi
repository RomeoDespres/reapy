import sys


def is_inside_reaper() -> bool:
    """
    Return whether ``reapy`` is imported from inside REAPER.
    """
    ...


from .tools import inside_reaper as inside_reaper
from . import reascript_api as reascript_api
from .core import *
from .core.reaper import *

__all__ = [
    # core.reapy_object
    "ReapyObject",
    "ReapyObjectList",
    #core.audio_accessor
    "AudioAccessor",
    # core.envelope
    "Envelope",
    "EnvelopeList",
    # core.fx
    "FX",
    "FXList",
    "FXParam",
    "FXParamsList",
    # core.item
    "CC",
    "CCList",
    "Item",
    "Note",
    "NoteList",
    "Source",
    "Take",
    # core.project
    "Marker",
    "Project",
    "Region",
    "TimeSelection",
    # core.track
    "AutomationItem",
    "Send",
    "Track",
    "TrackList",
    # core.window
    "MIDIEditor",
    "ToolTip",
    "Window",
    'add_reascript',
    'arm_command',
    'browse_for_file',
    'clear_console',
    'clear_peak_cache',
    'dB_to_slider',
    'delete_ext_state',
    'disarm_command',
    'get_armed_command',
    'get_command_id',
    'get_command_name',
    'get_exe_dir',
    'get_ext_state',
    'get_global_automation_mode',
    'get_ini_file',
    'get_last_touched_track',
    'get_main_window',
    'get_projects',
    'get_reaper_version',
    'get_resource_path',
    'has_ext_state',
    'open_project',
    'perform_action',
    'prevent_ui_refresh',
    'print',
    'reaprint',
    'remove_reascript',
    'rgb_from_native',
    'rgb_to_native',
    'set_ext_state',
    'set_global_automation_mode',
    'show_console_message',
    'show_message_box',
    'slider_to_dB',
    'test_api',
    'undo_block',
    'update_arrange',
    'update_timeline',
    'view_prefs',
    'audio',
    'midi',
    'ui',
    'defer',
    'at_exit',
]
