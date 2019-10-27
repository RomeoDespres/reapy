"""Define FX and FXParam classes."""

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import DistError, UndefinedFXParamError
import typing as ty


class FX(ReapyObject):
    """FX on a Track or a Take."""

    _class_name: str
    functions: ty.Dict[str, ty.Dict[str, ty.Callable[..., ty.Any]]]
    parent_id: str
    index: int

    def __init__(self,
                 parent: ty.Optional[ty.Union[reapy.Track, reapy.Take]] = None,
                 index: ty.Optional[int] = None,
                 parent_id: ty.Optional[str] = None) -> None:
        ...

    def _get_functions(self) -> ty.Dict[str, ty.Callable[..., ty.Any]]:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, ty.Union[str, int]]:
        ...

    def close_chain(self) -> None:
        """Close FX chain."""
        ...

    def close_floating_window(self) -> None:
        """Close FX floating window."""
        ...

    def close_ui(self) -> None:
        """Close user interface."""
        ...

    def copy_to_take(self, take: reapy.Take, index: int = 0) -> None:
        """
        Copy FX to take.

        Parameters
        ----------
        take : Take
            Destination take.
        index : int
            Index on destination take.

        See also
        --------
        FX.move_to_take
        """
        ...

    def copy_to_track(self, track: reapy.Track, index: int = 0) -> None:
        """
        Copy FX to track.

        Parameters
        ----------
        track : Track
            Destination track.
        index : int
            Index on destination track.

        See also
        --------
        FX.move_to_track
        """
        ...

    def delete(self) -> None:
        """Delete FX."""
        ...

    def disable(self) -> None:
        """Disable FX."""
        ...

    def enable(self) -> None:
        """Enable FX."""
        ...

    @property
    def is_enabled(self) -> bool:
        """
        Whether FX is enabled.

        :type: bool
        """
        ...

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        ...

    @property
    def is_online(self) -> bool:
        """
        Whether FX is online.

        :type: bool
        """
        ...

    @is_online.setter
    def is_online(self, online: bool) -> None:
        ...

    @property
    def is_ui_open(self) -> bool:
        """
        Whether FX user interface is open.

        :type: bool
        """
        ...

    @is_ui_open.setter
    def is_ui_open(self, open: bool) -> None:
        ...

    def make_offline(self) -> None:
        """Make FX offline."""
        ...

    def make_online(self) -> None:
        """Make FX online."""
        ...

    def move_to_take(self, take: reapy.Take, index: int = 0) -> None:
        """
        Move FX to take.

        Parameters
        ----------
        take : Take
            Destination take.
        index : int
            Index on destination take.

        See also
        --------
        FX.copy_to_take
        """
        ...

    def move_to_track(self, track: reapy.Track, index: int = 0) -> None:
        """
        Move FX to track.

        Parameters
        ----------
        track : Track
            Destination track.
        index : int
            Index on destination track.

        See also
        --------
        FX.copy_to_track
        """
        ...

    @property
    def n_inputs(self) -> int:
        """
        Number of inputs of FX.

        :type: int
        """
        ...

    @property
    def n_outputs(self) -> int:
        """
        Number of outputs of FX.

        :type: int
        """
        ...

    @property
    def n_params(self) -> int:
        """
        Number of parameters.

        :type: int
        """
        ...

    @property
    def n_presets(self) -> int:
        """
        Number of presets.

        :type: int
        """
        ...

    @property
    def name(self) -> str:
        """
        FX name.

        :type: str
        """
        ...

    def open_chain(self) -> None:
        """Open FX chain with focus on FX."""
        ...

    def open_floating_window(self) -> None:
        """Open FX floating window."""
        ...

    def open_ui(self) -> None:
        """Open FX user interface."""
        ...

    @property
    def params(self) -> reapy.FXParamsList:
        """
        List of parameters.

        :type: FXParamsList
        """
        ...

    @property
    def parent(self) -> ty.Union[reapy.Track, reapy.Take]:
        """
        FX parent.

        :type: Track or Take
        """
        ...

    @property
    def preset(self) -> str:
        """
        FX preset name.

        :type: str

        Attribute can be set by passing a str or int. In the first
        case, the str can either be a preset name or the path to a
        .vstpreset file. Otherwise, the int is the preset index.
        """
        ...

    @preset.setter
    def preset(self, preset: ty.Union[str, int]) -> None:
        """
        Set FX preset.

        Parameters
        ----------
        preset : str or int
            If str, preset name or path to .vstpreset file. If int,
            preset index. Set to -2 for factory preset, and -1 for user
            default preset.
        """
        ...

    @property
    def preset_index(self) -> int:
        """
        FX preset index.

        :type: int
        """
        ...

    @property
    def preset_file(self) -> str:
        """
        Path to FX preset file.

        :type: str
        """
        ...

    def use_previous_preset(self) -> None:
        """Use previous preset in the presets list."""
        ...

    def use_next_preset(self) -> None:
        """Use next preset in the presets list."""
        ...

    @property
    def window(self) -> ty.Optional[reapy.Window]:
        """
        Floating window associated to FX, if it exists.

        :type: Window or NoneType
        """
        ...


class FXList(ReapyObjectList):
    """
    Container class for a list of FXs.

    FXs can be accessed by name or index.

    Examples
    --------
    >>> fx_list = track.fxs
    >>> fx_list[0]
    FX(parent_id="(MediaTrack*)0x0000000006CDEBE0", index=0)
    >>> len(fx_list)
    1
    >>> fx_list["VST: ReaComp (Cockos)"]
    FX(parent_id="(MediaTrack*)0x0000000006CDEBE0", index=0)
    """

    _class_name = "FXList"
    parent: ty.Union[reapy.Track, reapy.Take]

    def __init__(self, parent: ty.Union[reapy.Track, reapy.Take]) -> None:
        ...

    @reapy.inside_reaper()
    def __delitem__(self, key: ty.Union[int, slice]) -> None:
        ...

    @ty.overload
    def __getitem__(self, i: ty.Union[int, str]) -> reapy.FX:
        ...

    @ty.overload
    def __getitem__(self, i: slice) -> ty.List[reapy.FX]:
        ...

    def __len__(self) -> int:
        ...

    @reapy.inside_reaper()
    def _get_items_from_slice(self, slice: slice) -> ty.List[reapy.FX]:
        ...

    def _get_fx_index(self, name: str) -> int:
        ...

    @property
    def _args(self) -> ty.Tuple[ty.Union[reapy.Track, reapy.Take]]:
        ...
