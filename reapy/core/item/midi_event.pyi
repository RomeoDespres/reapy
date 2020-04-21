import struct
import typing as ty
from enum import IntFlag, IntEnum
import typing_extensions as te

import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList

T1 = ty.TypeVar('T1', bound='MIDIEvent')


class CCShapeFlag(IntFlag):
    square: int
    linear: int
    slow_start_end: int
    fast_start: int
    fast_end: int
    beizer: int

    @classmethod
    def from_shape(cls, shape: 'CCShape') -> 'CCShapeFlag':
        """
        Get flags from int enum.

        Parameters
        ----------
        shape : CCShape
            or just int from 0 to 5

        Returns
        -------
        CCShapeFlag
        """
        ...


class CCShape(IntEnum):
    square: int
    linear: int
    slow_start_end: int
    fast_start: int
    fast_end: int
    beizer: int

    @classmethod
    def from_flag(cls, flag: CCShapeFlag) -> 'CCShape':
        """
        Get IntEnum from IntFlag.

        Parameters
        ----------
        flag : CCShapeFlag

        Returns
        -------
        CCShape
        """
        ...


MIDIEventDict = te.TypedDict(
    'MIDIEventDict', {
        'ppq': int,
        'selected': bool,
        'muted': bool,
        'cc_shape': CCShapeFlag,
        'buf': ty.List[int],
    }
)


class MIDIEventInfo(te.TypedDict):
    selected: bool
    muted: bool
    position: float
    raw_message: ty.List[int]
    ppq_position: int


class MIDIEvent(ReapyObject):
    """Abstract class for MIDI events."""
    index: int
    parent: reapy.Take

    def __init__(self, parent: reapy.Take, index: int) -> None:
        """
        Create event.

        Parameters
        ----------
        parent : Take
            Take to which the event belongs.
        index : int
            Event index. It is specific to the event type, which means
            a Note and a CC can have the same index.
        """
        ...

    @property
    def _args(self) -> ty.Tuple[reapy.Take, int]:
        ...

    @property
    def _del_name(self) -> str:
        ...

    @property
    def as_dict(self) -> ty.Tuple[MIDIEventDict, ...]:
        """
        Representation of event in a dict.

        Notes
        -----
        ⋅ Can be used for inserting along with event buffer.
        ⋅ For notes and CC with beizer curve returns list of 2 items.

        :type: Tuple[MIDIEventDict]
        """
        ...

    def delete(self) -> None:
        """Delete event from the take."""
        ...

    @property
    def infos(self) -> MIDIEventInfo:
        """
        Event info as dict.

        :type: MIDIEventInfo
            {'selected': bool,
            'muted': bool,
            'position': float,
            'message': List[int],
            'ppq_position': int}
        """
        ...

    def set(
        self,
        selected: ty.Optional[bool] = None,
        muted: ty.Optional[bool] = None,
        position: ty.Optional[float] = None,
        sort: ty.Optional[bool] = True,
        raw_message: ty.Optional[ty.List[int]] = None,
        *,
        time_unit: str = "seconds"
    ) -> None:
        """
        Set properties of event if needed.

        Note
        ----
        Optional arguments can be None, therefore will not be applied at all.

        Parameters
        ----------
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool, optional
            Whether to mute new note (default=False).
        position : float, optional
            position at take
        sort : bool, optional
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.
        raw_message : List[int], optional
            can be applied to every type of event, which leads to
            ignoring of the event-specific arguments.
        time_unit : str ("seconds as default")
            "beats"|"ppq"|"seconds" (default are seconds)
        """
        ...


class MIDIEventList(ReapyObjectList, ty.Generic[T1]):
    parent: reapy.Take

    def __init__(self, parent: reapy.Take) -> None:
        """
        Create event list.

        Parameters
        ----------
        parent : Take
            Take to which the event list belongs.
        """
        ...

    def __getitem__(self, key: int) -> T1:
        ...

    def __len__(self) -> int:
        ...

    @property
    def _args(self) -> ty.Tuple[reapy.Take]:
        ...

    @property
    def _elements_class(self) -> ty.Type[T1]:
        ...

    @property
    def _n_elements(self) -> str:
        ...


class CCInfo(MIDIEventInfo):
    channel_message: int
    channel: int
    messages: ty.Tuple[int, int]


class CC(MIDIEvent):
    """MIDI CC event."""

    @property
    def as_dict(self) -> ty.Tuple[MIDIEventDict, ...]:
        """
        Representation of event in a dict.

        Notes
        -----
        ⋅ Can be used for inserting along with event buffer.
        ⋅ For notes and CC with beizer curve returns list of 2 items.

        :type: Tuple[MIDIEventDict]
        """
        ...

    @property
    def channel(self) -> int:
        """
        CC channel between 0 and 15.

        :type: int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @channel.setter
    def channel(self, channel: int) -> None:
        ...

    @property
    def channel_message(self) -> int:
        """
        CC channel message.

        :type: int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @channel_message.setter
    def channel_message(self, channel_message: int) -> None:
        ...

    @property
    def _del_name(self) -> str:
        ...

    @property
    def infos(self) -> CCInfo:
        """
        Return infos about CC.

        :type: CCInfo
            selected: bool
            muted: bool
            position: float
            ppq_position: float
            raw_message: List[int]
            channel_message: int
            channel: int
            messages: Tuple[int, int]
        """
        ...

    @property
    def messages(self) -> ty.Tuple[int, int]:
        """
        CC messages.

        :type: 2-list of int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @messages.setter
    def messages(self, messages: ty.Tuple[int, int]) -> None:
        ...

    @property
    def muted(self) -> bool:
        """
        Whether CC is muted.

        :type: bool

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @muted.setter
    def muted(self, muted: bool) -> None:
        ...

    @property
    def position(self) -> float:
        """
        CC position in seconds.

        :type: float

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @position.setter
    def position(self, position: float) -> None:
        ...

    @property
    def selected(self) -> bool:
        """
        Whether CC is selected.

        :type: bool

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        ...

    @selected.setter
    def selected(self, selected: bool) -> None:
        ...

    def set(
        self,
        selected: ty.Optional[bool] = None,
        muted: ty.Optional[bool] = None,
        position: ty.Optional[float] = None,
        sort: ty.Optional[bool] = True,
        raw_message: ty.Optional[ty.List[int]] = None,
        channel_message: ty.Optional[int] = None,
        channel: ty.Optional[int] = None,
        messages: ty.Optional[ty.List[int]] = None,
        *,
        time_unit: str = "seconds"
    ) -> None:
        """
        Set properties of event if needed.

        Note
        ----
        Optional arguments can be None, therefore will not be applied at all.

        Parameters
        ----------
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool, optional
            Whether to mute new note (default=False).
        position : float, optional
            position at take
        sort : bool, optional
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.
        raw_message : List[int], optional
            can be applied to every type of event, which leads to
            ignoring of the event-specific arguments.
        channel_message : int, optional
            0xb0 for example
        channel : int, optional
        messages : Tuple[int, int], optional
            CC_num, value
        time_unit : str Optional
            "beats"|"ppq"|"seconds" (default are seconds)
        """
        ...

    @property
    def shape(self) -> CCShape:
        """
        Shape type and beizer tension.

        :type: Tuple[CCShape, float]
            shape can be passed as enum instance or as int
        """
        ...

    @shape.setter
    def shape(self, shape: CCShape) -> None:
        ...


class CCList(MIDIEventList[CC]):
    ...


class NoteInfo(MIDIEventInfo):
    end: float
    ppq_end: float
    channel: int
    pitch: int
    velocity: int


class Note(MIDIEvent):
    """MIDI note."""

    @property
    def end(self) -> float:
        """
        Note end in seconds.

        :type: float

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        ...

    @end.setter
    def end(self, end: float) -> None:
        ...

    @property
    def infos(self) -> NoteInfo:
        """
        Return infos about note.

        :type: NoteInfo
            selected: bool
            muted: bool
            position: float
            ppq_position: float
            raw_message: [0x9+ch, note, vel]
            end: float
            ppq_end: float
            channel: int
            pitch: int
            velocity: int
        """
        ...

    @property
    def pitch(self) -> int:
        """
        Note pitch between 0 and 127.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """

    @pitch.setter
    def pitch(self, pitch: int) -> None:
        ...

    def set(
        self,
        selected: ty.Optional[bool] = None,
        muted: ty.Optional[bool] = None,
        position: ty.Optional[float] = None,
        sort: ty.Optional[bool] = True,
        raw_message: ty.Optional[ty.List[int]] = None,
        end: ty.Optional[float] = None,
        channel: ty.Optional[int] = None,
        pitch: ty.Optional[int] = None,
        velocity: ty.Optional[int] = None,
        *,
        time_unit: str = "seconds"
    ) -> None:
        """
        Set properties of event if needed.

        Note
        ----
        Optional arguments can be None, therefore will not be applied at all.

        Parameters
        ----------
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool, optional
            Whether to mute new note (default=False).
        position : float, optional
            position at take
        sort : bool, optional
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.
        raw_message : List[int], optional
            can be applied to every type of event, which leads to
            ignoring of the event-specific arguments.
        end : float
        channel : int
        pitch : int
        velocity : int
        time_unit : str ("seconds as default")
            "beats"|"ppq"|"seconds" (default are seconds)
        """
        ...

    @property
    def start(self) -> float:
        """
        Note start in seconds.

        :type: float

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        ...

    @start.setter
    def start(self, start: float) -> None:
        ...

    @property
    def velocity(self) -> int:
        """
        Note velocity between 0 and 127.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        ...

    @velocity.setter
    def velocity(self, velocity: int) -> None:
        ...


class NoteList(MIDIEventList[Note]):
    ...


class TextSysexInfo(MIDIEventInfo):
    type_: int


class TextSysex(MIDIEvent):
    """Abstract class for Text or Sysex events."""

    @property
    def infos(self) -> TextSysexInfo:
        """
        Event info as dict.

        :type: TextSysexInfo
            {'selected': bool,
            'muted': bool,
            'position': float,
            'message': List[int],
            'ppq_position': float,
            'type_': int
            }
        """
        ...

    def set(
        self,
        selected: ty.Optional[bool] = None,
        muted: ty.Optional[bool] = None,
        position: ty.Optional[float] = None,
        sort: ty.Optional[bool] = True,
        raw_message: ty.Optional[ty.List[int]] = None,
        type_: ty.Optional[int] = None,
        *,
        time_unit: str = "seconds"
    ) -> None:
        """
        Set properties of event if needed.

        Notes
        -----
        ⋅ Optional arguments can be None, therefore will not be applied at all
        ⋅ type_ is NOT optional when new raw_message is assigned

        Parameters
        ----------
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool, optional
            Whether to mute new note (default=False).
        position : float, optional
            position at take
        sort : bool, optional
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.
        raw_message : List[int], optional
            can be applied to every type of event, which leads to
            ignoring of the event-specific arguments.
        type_ : int, optional
            -1:sysex (msg should not include bounding F0..F7),
            1-14:MIDI text event types,
            15=REAPER notation event.
        time_unit : str ("seconds as default")
            "beats"|"ppq"|"seconds" (default are seconds)
        """
        ...

    @property
    def type_(self) -> int:
        """
        Meta event type

        :type: int
            -1:sysex (msg should not include bounding F0..F7),
            1-14:MIDI text event types,
            15=REAPER notation event.
        """
        ...

    @type_.setter
    def type_(self, type_: int) -> None:
        ...


class TextSysexList(MIDIEventList[TextSysex]):
    ...
