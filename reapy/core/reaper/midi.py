import reapy.reascript_api as RPR


def reinit():
    """Reset all MIDI devices."""
    RPR.midi_reinit()
