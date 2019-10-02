"""Audio handling functions."""

import reapy
import reapy.reascript_api as RPR
import typing as ty


def get_input_latency(unit: str = "second") -> float:
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
    ...


@reapy.inside_reaper()
def get_input_names() -> ty.List[str]:
    """
    Return names of all input channels.

    Returns
    -------
    names : list of str
        Names of input channels.
    """
    ...


def get_n_inputs() -> int:
    """
    Return number of audio inputs.

    Returns
    -------
    n_inputs : int
        Number of audio inputs.
    """
    ...


def get_n_outputs() -> int:
    """
    Return number of audio outputs.

    Returns
    -------
    n_outputs : int
        Number of audio outputs.
    """
    ...


def get_output_latency(unit: str = "second") -> float:
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
    ...


@reapy.inside_reaper()
def get_output_names() -> ty.Tuple[str, ...]:
    """
    Return names of all output channels.

    Returns
    -------
    names : list of str
        Names of output channels.
    """
    ...


def init() -> None:
    """
    Open all audio and MIDI devices (if not opened).
    """
    ...


def is_prebuffer() -> bool:
    """
    Return whether audio is in pre-buffer (threadsafe).

    Returns
    -------
    is_prebuffer : bool
        Whether audio is in pre-buffer.
    """
    ...


def is_running() -> bool:
    """
    Return whether audio is running (threadsafe).

    Returns
    -------
    is_running : bool
        Whether audio is running.
    """
    ...


def quit() -> None:
    """
    Close all audio and MIDI devices (if opened).
    """
    ...
