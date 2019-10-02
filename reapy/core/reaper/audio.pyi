"""Audio handling functions."""

import reapy
import reapy.reascript_api as RPR


def get_input_latency(unit="second"):
    """
    Return input latency.

    Parameters
    ----------
    unit : {"sample", "second"}
        Whether to return latency in samples or seconds
        (default="second").

    Returns
    -------
    latency : float
        Input latency.
    """
    latency, out_latency = RPR.GetInputOutputLatency(0, 0)
    if unit == "second":
        # Small hack because RPR.GetInputLatency doesn't exist...
        latency *= RPR.GetOutputLatency() / out_latency
    return latency


@reapy.inside_reaper()
def get_input_names():
    """
    Return names of all input channels.

    Returns
    -------
    names : list of str
        Names of input channels.
    """
    n_channels = reapy.audio.get_n_inputs()
    return tuple(map(RPR.GetInputChannelName, range(n_channels)))


def get_n_inputs():
    """
    Return number of audio inputs.

    Returns
    -------
    n_inputs : int
        Number of audio inputs.
    """
    n_inputs = RPR.GetNumAudioInputs()
    return n_inputs


def get_n_outputs():
    """
    Return number of audio outputs.

    Returns
    -------
    n_outputs : int
        Number of audio outputs.
    """
    n_outputs = RPR.GetNumAudioOutputs()
    return n_outputs


def get_output_latency(unit="second"):
    """
    Return output latency.

    Parameters
    ----------
    unit : {"sample", "second"}
        Whether to return latency in samples or seconds
        (default="second").

    Returns
    -------
    latency : float
        Output latency.
    """
    latency, out_latency = RPR.GetInputOutputLatency(0, 0)
    if unit == "second":
        latency = RPR.GetOutputLatency()
    else:
        latency = RPR.GetInputOutputLatency(0, 0)[1]
    return latency


@reapy.inside_reaper()
def get_output_names():
    """
    Return names of all output channels.

    Returns
    -------
    names : list of str
        Names of output channels.
    """
    n_channels = reapy.audio.get_n_outputs()
    return tuple(map(RPR.GetOutputChannelName, range(n_channels)))


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
