from .core.reaper import *
from .core import *
from . import reascript_api as reascript_api
from .tools import (
    connect, connect_to_default_machine, dist_api_is_enabled, inside_reaper,
    reconnect
)
import sys


def is_inside_reaper() -> bool:
    """
    Return whether ``reapy`` is imported from inside REAPER.
    """
    ...


__all__ = [
    # core.reapy_object
    "ReapyObject",
    "ReapyObjectList",
    # core.audio_accessor
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
    "Item",
    "MIDIEvent",
    "MIDIEventList",
    "CC",
    "CCList",
    "Note",
    "NoteList",
    "TextSysex",
    "TextSysexInfo",
    "TextSysexList",
    "CCShapeFlag",
    "CCShape",
    "MIDIEventDict",
    "MIDIEventInfo",
    "CCInfo",
    'NoteInfo',
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
    "get_project_by_name",
    # core.window
    "MIDIEditor",
    "ToolTip",
    "Window",
    # core.reaper
    'add_reascript',
    'arm_command',
    'browse_for_file',
    'clear_console',
    'clear_peak_cache',
    'close_project_tab',
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
    'get_user_inputs',
    'has_ext_state',
    'new_project_tab',
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
    'validate_id',
    'audio',
    'midi',
    'ui',
    'defer',
    'at_exit',
    # tools
    'connect',
    'connect_to_default_machine',
    'dist_api_is_enabled',
    'inside_reaper',
    'reconnect',
]
