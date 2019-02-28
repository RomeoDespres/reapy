import reapy
import reapy.reascript_api as RPR


def get_active_editor():
    """
    Return active MIDI editor, or None if no editor is active.

    Returns
    -------
    editor : MIDIEditor or None
        Active MIDI editor, or None if no editor is active.
    """
    editor = reapy.MIDIEditor(RPR.MIDIEditor_GetActive())
    if not editor._is_defined:
        editor = None
    return editor

def reinit():
    """Reset all MIDI devices."""
    RPR.midi_reinit()
