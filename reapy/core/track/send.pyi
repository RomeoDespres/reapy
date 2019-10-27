import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class Send(ReapyObject):

    _class_name = "Send"
    index: int
    track_id: ty.Union[str, int]
    type: str

    def __init__(self,
                 track: ty.Optional[reapy.Track] = None,
                 index: int = 0,
                 track_id: ty.Optional[ty.Union[str, int]] = None,
                 type: str = "send") -> None:
        ...

    def _get_int_type(self) -> int:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, object]:
        ...

    def delete(self) -> None:
        """
        Delete send.
        """
        ...

    @reapy.inside_reaper()
    def flip_phase(self) -> None:
        """
        Toggle whether phase is flipped.
        """
        ...

    def get_info(self, param_name: str) -> float:
        ...

    @property
    def is_mono(self) -> bool:
        """
        Whether send is mono or stereo.

        :type: bool
        """
        ...

    @is_mono.setter
    def is_mono(self, mono: bool) -> None:
        ...

    @property
    def is_muted(self) -> bool:
        """
        Whether send is muted.

        :type: bool
        """
        ...

    @is_muted.setter
    def is_muted(self, is_muted: bool) -> None:
        """
        Mute or unmute send.

        Parameters
        ----------
        is_muted : bool
            Whether to mute or unmute send.
        """
        ...

    @property
    def is_phase_flipped(self) -> bool:
        """
        Whether send phase is flipped (i.e. signal multiplied by -1).

        :type: bool
        """
        ...

    @is_phase_flipped.setter
    def is_phase_flipped(self, flipped: bool) -> None:
        ...

    def mute(self) -> None:
        """
        Mute send.
        """
        ...

    @property
    def pan(self) -> float:
        """
        Send pan (from -1=left to 1=right).

        :type: float
        """
        ...

    @pan.setter
    def pan(self, pan: float) -> None:
        """
        Set send pan.

        Parameters
        ----------
        pan : float
            New pan between -1 (left) and 1 (right).
        """
        ...

    def set_info(self, param_name: str, value: float) -> None:
        ...

    @property
    def source_track(self) -> reapy.Track:
        """
        Source track.

        :type: Track
        """
        ...

    def unmute(self) -> None:
        """
        Unmute send.
        """
        ...

    @property
    def volume(self) -> float:
        """
        Send volume.

        :type: float
        """
        ...

    @volume.setter
    def volume(self, volume: float) -> None:
        ...
