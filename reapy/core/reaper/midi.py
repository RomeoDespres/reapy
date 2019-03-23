import reapy
import reapy.reascript_api as RPR
from reapy.tools import Program


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


def get_input_names():
    """
    Return names of all input channels.

    Returns
    -------
    names : list of str
        Names of input channels.
    """
    code = """
    n_channels = reapy.midi.get_n_inputs()
    names = [RPR.GetMIDIInputName(i, "", 2048)[2] for i in range(n_channels)]
    """
    names, = Program(code, "names").run()
    return names


def get_max_inputs():
    """
    Return maximum number of MIDI inputs.

    Returns
    -------
    max_inputs : int
        Maximum number of MIDI inputs.
    """
    max_inputs = RPR.GetMaxMidiInputs()
    return max_inputs


def get_max_outputs():
    """
    Return maximum number of MIDI outputs.

    Returns
    -------
    max_outputs : int
        Maximum number of MIDI outputs.
    """
    max_outputs = RPR.GetMaxMidiOutputs()
    return max_outputs


def get_n_inputs():
    """
    Return number of MIDI inputs.

    Returns
    -------
    n_inputs : int
        Number of MIDI inputs.
    """
    n_inputs = RPR.GetNumMIDIInputs()
    return n_inputs


def get_n_outputs():
    """
    Return number of MIDI outputs.

    Returns
    -------
    n_outputs : int
        Number of MIDI outputs.
    """
    n_outputs = RPR.GetNumMIDIOutputs()
    return n_outputs


def get_output_names():
    """
    Return names of all output channels.

    Returns
    -------
    names : list of str
        Names of output channels.
    """
    code = """
    n_channels = reapy.midi.get_n_outputs()
    names = [RPR.GetMIDIOutputName(i, "", 2048)[2] for i in range(n_channels)]
    """
    names, = Program(code, "names").run()
    return names


def reinit():
    """Reset all MIDI devices."""
    RPR.midi_reinit()
