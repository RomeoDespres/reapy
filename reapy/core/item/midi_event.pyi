import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
import typing as ty
import typing_extensions as te

T = ty.TypeVar('T')


class MIDIEvent(ReapyObject):
    """Abstract class for MIDI events."""
    parent: reapy.Take
    index: int

    def __init__(self, parent: reapy.Take, index: int):
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


class MIDIEventList(ReapyObjectList, ty.Generic[T]):
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

    def __getitem__(self, key: int) -> T:
        ...

    def __len__(self) -> int:
        ...

    @property
    def _args(self) -> ty.Tuple[reapy.Take]:
        ...

    @property
    def _elements_class(self) -> ty.Type[T]:
        ...

    @property
    def _n_elements(self) -> str:
        ...


CC_INFOS_T = te.TypedDict(
    'CC_INFOS_T', {
        "selected": bool,
        "muted": bool,
        "position": float,
        "channel": int,
        "channel_message": int,
        "messages": ty.Tuple[int, int]
    })


class CC(MIDIEvent):
    """MIDI CC event."""
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

    @reapy.inside_reaper()
    @property
    def infos(self) -> CC_INFOS_T:
        """
        Return infos about CC.

        Keys are {"selected", "muted", "position", "channel",
        "channel_message", "messages"}.

        :type: dict
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


class CCList(MIDIEventList[CC]):

    _elements_class: ty.Type[CC]
    _n_elements: str


NOTE_INFOS_T = te.TypedDict(
    'NOTE_INFOS_T', {
        "selected": bool,
        "muted": bool,
        "position": float,
        "channel": int,
        "pitch": int,
        "velocity": int
    })


class Note(MIDIEvent):
    """MIDI note."""
    @property
    def channel(self) -> int:
        """
        Note channel between 0 and 15.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        ...

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

    @property
    def infos(self) -> NOTE_INFOS_T:
        """
        Return infos about note.

        Keys are {"selected", "muted", "start", "end", "channel",
        "pitch", "velocity"}.

        :type: dict
        """
        ...

    @property
    def muted(self) -> bool:
        """
        Whether note is muted.

        :type: bool

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
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
        ...

    @property
    def selected(self) -> bool:
        """
        Whether note is selected.

        :type: bool

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
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


class NoteList(MIDIEventList[Note]):

    _elements_class: ty.Type[Note]
    _n_elements: str
