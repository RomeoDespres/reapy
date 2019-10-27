"""User interface-related functions."""

import reapy
import reapy.reascript_api as RPR


def get_color_theme() -> str:
    """
    Return path to last color theme file.

    Returns
    -------
    color_theme : str
        Path to last color theme file.
    """
    ...


def get_leftmost_track_in_mixer() -> reapy.Track:
    """Return leftmost track in mixer."""
    ...


def set_color_theme(path: str) -> None:
    """
    Set REAPER color theme.

    Parameters
    ----------
    path : str
        Path to color theme file.
    """
    ...


def set_leftmost_track_in_mixer(track: reapy.Track) -> None:
    """Set leftmost track in mixer.

    The actual leftmost track in mixer might be different after
    calling if there is not enough tracks to the right of the
    specified track.

    Parameters
    ----------
    track : Track
        Track to set as leftmost track in mixer.
    """
    ...
