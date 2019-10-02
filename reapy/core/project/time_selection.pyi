import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class TimeSelection(ReapyObject):

    _class_name = "TimeSelection"
    project_id: int

    def __init__(self,
                 parent_project: ty.Optional[reapy.Project] = None,
                 parent_project_id: ty.Optional[int] = None) -> None:
        ...

    def _get_infos(self) -> ty.Tuple[ty.Any, ...]:
        """
        Return infos as returned by RPR.GetSet_LoopTimeRange2.

        Returns
        -------
        infos : tuple
            Time selection infos.
        """
        ...

    def _set_start_end(self,
                       start: ty.Optional[float] = None,
                       end: ty.Optional[float] = None) -> None:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, int]:
        ...

    @reapy.inside_reaper()
    @property
    def end(self) -> float:
        """
        Return time selection end in seconds.

        Returns
        -------
        end : float
            Time selection end in seconds.
        """
        ...

    @end.setter
    def end(self, end: float) -> None:
        """
        Set time selection end.

        Parameters
        ----------
        end : float
            Time selection end in seconds.
        """
        ...

    @property
    def is_looping(self) -> bool:
        """
        Return whether looping is enabled.

        Returns
        -------
        looping : bool
            Whether looping is enabled.
        """
        ...

    @is_looping.setter
    def is_looping(self, is_looping: bool) -> None:
        """
        Sets whether time selection should loop.

        Parameters
        ----------
        looping : bool
            Whether time selection should loop.
        """
        ...

    @reapy.inside_reaper()
    @property
    def length(self) -> float:
        """
        Return time selection length in seconds.

        Returns
        -------
        length : float
            Time selection length in seconds.
        """
        ...

    @length.setter
    def length(self, length: float) -> None:
        """
        Set time selection length (by moving its end).

        Parameters
        ----------
        length : float
            Time selection length in seconds.
        """
        ...

    def loop(self) -> None:
        """
        Enable time selection looping.

        See also
        --------
        TimeSelection.is_looping
        TimeSelection.unloop
        """
        ...

    @reapy.inside_reaper()
    @property
    def start(self) -> float:
        """
        Return time selection start in seconds.

        Returns
        -------
        start : float
            Time selection start in seconds.
        """
        ...

    @start.setter
    def start(self, start: float) -> None:
        """
        Set time selection start.

        Parameters
        ----------
        start : float
            New time selection start.
        """
        ...

    def shift(self, direction: str = "") -> None:
        """
        Shift time selection.

        Parameters
        ----------
        direction : {"right", "left"}
            Direction to which time selection will be shifted. Nothing
            happens if direction is neither "right" nor "left". Note
            that the shift size depends on whether snap is enabled
            and of the zoom level.
        """
        ...

    def unloop(self) -> None:
        """
        Disable time selection looping.

        See also
        --------
        TimeSelection.is_looping
        TimeSelection.loop
        """
        ...
