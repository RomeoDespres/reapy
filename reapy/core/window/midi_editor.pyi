import reapy
import reapy.reascript_api as RPR
from .window import Window
import typing as ty


class MIDIEditor(Window):
    def _get_int_setting(self, setting: str) -> int:
        ...

    def _get_str_setting(self, setting: str) -> str:
        ...

    @property
    def last_clicked_cc_lane(self) -> int:
        """
        Last clicked CC lane.

        :type: int
        """
        ...

    @property
    def last_clicked_cc_lane_name(self) -> str:
        """
        Last clicked CC lane name ("velocity", "pitch", etc.).

        :type: str
        """
        ...

    @property
    def active_note_row(self) -> int:
        """
        Active note row (between 0 and 127).

        :type: int
        """
        ...

    @property
    def default_channel(self) -> int:
        """
        Default note channel (between 0 and 15).

        :type: int
        """
        ...

    @property
    def default_length(self) -> int:
        """
        Default note length in MIDI ticks.

        :type: int
        """
        ...

    @property
    def default_velocity(self) -> int:
        """
        Default note velocity (between 0 and 127).

        :type: int
        """
        int

    @property
    def is_scale_enabled(self) -> bool:
        """
        Whether scale is enabled in editor.

        :type: bool
        """
        ...

    @property
    def is_snap_enabled(self) -> bool:
        """
        Whether snap is enabled in editor.

        :type: bool
        """
        ...

    @property
    def mode(self) -> str:
        """
        Mode of MIDI editor.

        :type: {"piano roll", "event list"}
        """
        ...

    def perform_action(self, action_id: int):
        """
        Perform action (from MIDI Editor section).

        Parameters
        ----------
        action_id : int
            Action ID.
        """
        ...

    @property
    def scale_type(self) -> str:
        """
        Scale type ID.

        :type: str
        """
        ...

    @property
    def scale_root(self) -> int:
        """
        Scale root (between 0 and 12, 0=C).

        :type: int
        """
        ...

    @property
    def take(self) -> reapy.Take:
        """
        Take currently edited.

        :type: Take
        """
        ...
