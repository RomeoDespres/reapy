from enum import IntEnum, IntFlag

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import UndefinedEnvelopeError
import typing as ty


class RecMode(IntEnum):

    """Record mode of Track enum.

    Attributes
    ----------
    input_
    input_midi_overdub
    input_midi_replace
    none
    out_midi
    out_mono
    out_mono_laten_cmp
    out_stereo
    out_stereo_laten_cmp
    """

    input_: int
    out_stereo: int
    none: int
    out_stereo_laten_cmp: int
    out_midi: int
    out_mono: int
    out_mono_laten_cmp: int
    input_midi_overdub: int
    input_midi_replace: int


class RecMonitor(IntFlag):

    """Bit flags for setting record monitoring.

    Note
    ----
    top 3 bits are track option
    low 2 bits are items option
    track|item
    0b000 00

    Attributes
    ----------
    items_rec_off
    items_rec_on
    normal
    not_while_play
    off
    """

    off: int
    normal: int
    not_while_play: int
    items_rec_off: int
    items_rec_on: int

    def __or__(self, other: object) -> 'RecMonitor':
        """Return combined flags.

        Returns
        -------
        int

        Raises
        ------
        AttributeError
            if two items or two track flags are combined
        """
        ...

    @classmethod
    def _resolve_flags(cls, flags: 'RecMonitor') -> ty.Tuple[int, int]: ...

    def set_mode(self, track: 'Track', flags: 'RecMonitor') -> None:
        """Set monitoring mode on track depends on flags.

        Parameters
        ----------
        track : reapy.Track
            to set mode on
        flags : RecMonitor
        """
        ...

    def get_mode(self, track: 'Track') -> ty.Tuple[
            ty.Optional['RecMonitor'],
            ty.Optional['RecMonitor']]:
        """Get track monitor mode as tuple of modes.

        Parameters
        ----------
        track : reapy.Track

        Returns
        -------
        Tuple[RecMonitor, RecMonitor]
            first is track, second — item
        """
        ...

    def get_mode_flags(self, track: 'Track') -> 'RecMonitor':
        """Get track monitor mode as combined flags.

        Parameters
        ----------
        track : reapy.Track

        Returns
        -------
        RecMonitor
        """
        ...


class SoloState(IntEnum):

    """Solo mode of Track enum.

    Attributes
    ----------
    not_soloed
    safe_soloed
    safe_soloed_in_place
    soloed
    soloed_in_place
    """

    not_soloed: int
    soloed: int
    soloed_in_place: int
    safe_soloed: int
    safe_soloed_in_place: int

    def __nonzero__(self) -> bool: ...


class Track(ReapyObject):
    """
    REAPER Track.

    Parameters
    ----------
    id : str or int
        If str, can either be a ReaScript ID (usually looking like
        ``"(MediaTrack*)0x00000000110A1AD0"``), or a track name. In
        that case, ``project`` must be specified.
        If int, the index of the track. In that case, ``project`` must
        be specified.
    project : Project
        Parent project of the track. Only necessary to retrieve a
        track from its name or index.

    Examples
    --------
    In most cases, accessing tracks is better done directly from
    the parent Project:

    >>> project = reapy.Project()
    >>> project.tracks[0]
    Track("(MediaTrack*)0x00000000110A1AD0")
    >>> project.tracks["PIANO"]  # This is actually the same track
    Track("(MediaTrack*)0x00000000110A1AD0")

    But the same track can also directly be instantiated with:

    >>> reapy.Track(0, project)
    Track("(MediaTrack*)0x00000000110A1AD0")

    or

    >>> reapy.Track("PIANO")
    Track("(MediaTrack*)0x00000000110A1AD0")
    """
    id: str
    _project: reapy.Project

    def __init__(
        self, id: str, project: ty.Optional[reapy.Project] = None
    ) -> None:
        ...

    @property
    def _args(self) -> ty.Tuple[ty.Union[str, int]]:
        ...

    def _get_project(self) -> reapy.Project:
        """
        Return parent project of track.

        Should only be used internally; one should directly access
        Track.project instead of calling this method.
        """
        ...

    def add_audio_accessor(self) -> reapy.AudioAccessor:
        """
        Create audio accessor and return it.

        Returns
        -------
        audio_accessor : AudioAccessor
            Audio accessor on track.
        """
        ...

    def add_fx(
        self, name: str, input_fx: bool = False, even_if_exists: bool = True
    ) -> reapy.FX:
        """
        Add FX to track and return it.

        Parameters
        ----------
        name : str
            FX name.
        input_fx : bool, optional
            Whether the FX should be an input (aka recording) FX or a
            standard FX (default=False). Note that if the track is the
            master track, input_fx=True will create a monitoring FX.
        even_if_exists : bool, optional
            Whether the FX should be added even if there already is an
            instance of the same FX on the track (default=True).

        Returns
        -------
        fx : FX
            New FX on track (or previously existing instance of FX if
            even_if_exists=False).

        Raises
        ------
        ValueError
            If there is no FX with the specified name.
        """
        ...

    def add_item(
        self,
        start: float = 0,
        end: ty.Optional[float] = None,
        length: float = 0
    ) -> reapy.Item:
        """
        Create new item on track and return it.

        Parameters
        ----------
        start : float, optional
            New item start in seconds (default=0).
        end : float, optional
            New item end in seconds (default None). If None, `length`
            is used instead.
        length : float, optional
            New item length in seconds (default 0).

        Returns
        -------
        item : Item
            New item on track.
        """
        ...

    def add_midi_item(
        self, start: float = 0, end: float = 1, quantize: bool = False
    ) -> reapy.Item:
        """
        Add empty MIDI item to track and return it.

        Parameters
        ----------
        start : float, optional
            New item start in seconds (or beats if `quantize`=True).
        end : float, optional
            New item end in seconds (or beats if `quantize`=True).
        quantize : bool, optional
            Whether to count time in beats (True) or seconds (False,
            default).
        """
        ...

    def add_send(
        self, destination: ty.Optional[reapy.Track] = None
    ) -> reapy.Track:
        """
        Add send to track and return it.

        Parameters
        ----------
        destination : Track or None
            Send destination (default=None). If None, destination is
            set to hardware output.

        Returns
        -------
        send : Send
            New send on track.
        """
        ...

    @property
    def automation_mode(self) -> str:
        """
        Track automation mode.

        One of the following values:
            "latch"
            "latch preview"
            "read"
            "touch"
            "trim/read"
            "write"

        :type: str
        """
        ...

    @automation_mode.setter
    def automation_mode(self, mode: str) -> None:
        """
        Set track automation mode.

        Parameters
        -------
        mode : str
            One of the following values:
                "latch"
                "latch preview"
                "read"
                "touch"
                "trim/read"
                "write"
        """
        ...

    @property
    def color(self) -> ty.Tuple[int, int, int]:
        """
        Track color in RGB format.

        :type: tuple of int
        """
        ...

    @color.setter
    def color(self, color: ty.Tuple[int, int, int]) -> None:
        """
        Set track color to `color`

        Parameters
        ----------
        color : tuple
            Triplet of integers between 0 and 255 corresponding to RGB
            values.
        """
        ...

    def delete(self) -> None:
        """
        Delete track.
        """
        ...

    @property
    def depth(self) -> int:
        """
        Track depth.

        :type: int
        """
        ...

    @property
    def envelopes(self) -> reapy.EnvelopeList:
        """
        List of envelopes on track.

        :type: EnvelopeList
        """
        ...

    @property
    def fxs(self) -> reapy.FXList:
        """
        List of FXs on track.

        :type: FXList
        """
        ...

    @property
    def fxs_enabled(self) -> bool:
        """Whether fx chain is enabled.

        :type: bool
        """

    @fxs_enabled.setter
    def fxs_enabled(self, state: bool) -> None: ...

    def get_info_string(self, param_name: str) -> str:
        ...

    def get_info_value(self, param_name: str) -> float:
        ...

    @property
    def GUID(self) -> str:
        """
        Track's GUID.

        16-byte GUID, can query or update.
        If using a _String() function, GUID is a string {xyz-...}.

        :type: str
        """
        ...

    @GUID.setter
    def GUID(self, guid_string: str) -> None:
        ...

    @property
    def icon(self) -> str:
        """
        Track icon.

        Full filename, or relative to resource_path/data/track_icons.

        :type: str
        """
        ...

    @icon.setter
    def icon(self, filename: str) -> None:
        ...

    @property
    def instrument(self) -> ty.Optional[reapy.FX]:
        """
        First instrument FX on track if it exists, else None.

        :type: FX or None
        """
        ...

    @property
    def items(self) -> ty.List[reapy.Item]:
        """
        List of items on track.

        :type: list of Item
        """
        ...

    @property
    def is_muted(self) -> bool:
        """
        Whether track is muted.

        Can be manually set to change track state.
        """
        ...

    @is_muted.setter
    def is_muted(self, muted: bool) -> None:
        ...

    @property
    def is_selected(self) -> bool:
        """
        Whether track is selected.

        :type: bool
        """
        ...

    @is_selected.setter
    def is_selected(self, selected: bool) -> None:
        """
        Select or unselect track.

        Parameters
        ----------
        selected : bool
            Whether to select or unselect track.
        """
        ...

    @property
    def is_solo(self) -> bool:
        """
        Whether track is solo.

        Can be manually set to change track state.
        """
        ...

    @is_solo.setter
    def is_solo(self, solo: bool) -> None:
        ...

    def make_only_selected_track(self) -> None:
        """
        Make track the only selected track in parent project.
        """
        ...

    @property
    def midi_note_names(self) -> ty.List[str]:
        ...

    @property
    def monitor_state(self) -> RecMonitor:
        """Track monitoring settings as bit-flags.

        Note
        ----
        Flags of track and items monitoring mode can be combined.
        If not, track or items monitoring mode not assigned.

        :type: RecMonitor
        """
        ...

    @monitor_state.setter
    def monitor_state(self, state: RecMonitor) -> None: ...

    @property
    def monitor_state_tuple(self) -> ty.Tuple[
            ty.Optional[RecMonitor],
            ty.Optional[RecMonitor]]:
        """Track monitoring settings as tuple.

        :type: Tuple[Optional[RecMonitor], Optional[RecMonitor]]
        """
        ...

    def mute(self) -> None:
        """Mute track (do nothing if track is already muted)."""
        ...

    @property
    def mute_state(self) -> bool:
        """Track mute state.

        Returns
        -------
        bool
        """
        ...

    @mute_state.setter
    def mute_state(self, state: bool) -> None: ...

    @property
    def n_channels(self) -> int:
        """Number of track channels.

        :type: int
        """
        ...

    @property
    def n_envelopes(self) -> int:
        """
        Number of envelopes on track.

        :type: int
        """
        ...

    @property
    def n_fxs(self) -> int:
        """
        Number of FXs on track.

        :type: int
        """
        ...

    @property
    def n_hardware_sends(self) -> int:
        """
        Number of hardware sends on track.

        :type: int
        """
        ...

    @property
    def n_items(self) -> int:
        """
        Number of items on track.

        :type: int
        """
        ...

    @property
    def n_receives(self) -> int:
        ...

    @property
    def n_sends(self) -> int:
        ...

    @property
    def name(self) -> str:
        """
        Track name.

        Name is "MASTER" for master track, "Track N" if track has no
        name.

        :type: str
            Track name .
        """
        ...

    @name.setter
    def name(self, track_name: str) -> None:
        ...

    @property
    def parent_track(self) -> ty.Optional[reapy.Track]:
        """
        Parent track, or None if track has none.

        :type: Track or NoneType
        """
        ...

    @property
    def project(self) -> reapy.Project:
        """
        Track parent project.

        :type: Project
        """
        ...

    @property
    def phase_state(self) -> bool:
        """Phase invert state.

        Returns
        -------
        bool
        """
        ...

    @phase_state.setter
    def phase_state(self, state: bool) -> None: ...

    @property
    def recarm_state(self) -> bool:
        """Recarm state of the Track."""
        ...

    @recarm_state.setter
    def recarm_state(self, state: bool) -> None: ...

    @property
    def recmode_state(self) -> RecMode:
        """Record mode of the Track.

        :type: RecMode
        """
        ...

    @recmode_state.setter
    def recmode_state(self, state: ty.Union[bool, RecMode]) -> None: ...

    def select(self) -> None:
        """
        Select track.
        """
        ...

    @property
    def sends(self) -> ty.List[reapy.Send]:
        ...

    def set_info_value(self, param_name: str, value: int) -> None:

    def set_info_string(self, param_name: str, param_string: str) -> None:
        ...

    def solo(self) -> None:
        """Solo track (do nothing if track is already solo)."""
        ...

    @property
    def solo_state(self):
        """SummarySolo state of the Track

        :type: SoloState
        """
        ...

    @solo_state.setter
    def solo_state(self, state: SoloState) -> None: ...

    def toggle_mute(self) -> None:
        """Toggle mute on track."""
        ...

    def toggle_solo(self) -> None:
        """Toggle solo on track."""
        ...

    def unmute(self) -> None:
        """Unmute track (do nothing if track is not muted)."""
        ...

    def unselect(self) -> None:
        """
        Unselect track.
        """
        ...

    def unsolo(self) -> None:
        """Unsolo track (do nothing if track is not solo)."""
        ...

    @property
    def visible_fx(self) -> reapy.FX:
        """
        Visible FX in FX chain if any, else None.

        :type: FX or NoneType
        """
        ...


class TrackList(ReapyObjectList):
    """
    Container for a project's track list.

    Examples
    --------
    >>> tracks = project.tracks
    >>> len(tracks)
    4
    >>> tracks[0].name
    'Kick'
    >>> for track in tracks:
    ...     print(track.name)
    ...
    'Kick'
    'Snare'
    'Hi-hat'
    'Cymbal"
    """
    parent: reapy.Project

    def __init__(self, parent: reapy.Project) -> None:
        """
        Create track list.

        Parameters
        ----------
        parent : Project
            Parent project.
        """
        ...

    @ty.overload
    def __getitem__(self, key: str) -> Track:
        ...

    @ty.overload
    def __getitem__(self, key: int) -> Track:
        ...

    @ty.overload
    def __getitem__(self, key: slice) -> ty.List[Track]:
        ...

    def __delitem__(self, key: ty.Union[int, slice]) -> None:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> ty.Iterator[reapy.Track]:
        ...

    @property
    def _args(self) -> ty.Tuple[reapy.Project]:
        ...

    def _get_items_from_slice(self, slice: slice) -> ty.List[Track]:
        ...
