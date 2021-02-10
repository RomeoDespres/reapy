import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class Take(ReapyObject):

    _class_name = "Take"
    id: str

    def __init__(self, id: str) -> None:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    @property
    def _args(self) -> ty.Tuple[str]:
        ...

    def add_audio_accessor(self) -> reapy.AudioAccessor:
        """
        Create audio accessor and return it.

        Returns
        -------
        audio_accessor : AudioAccessor
            Audio accessor on take.
        """
        ...

    def add_event(self,
                  message: ty.Iterable[int],
                  position: float, unit: str = "seconds") -> None:
        """
        Add generic event to the take at position.

        Note
        ----
        ⋅ No sort events during this call
        ⋅ Inserting a notes within this function causes problems
            (wrong timing of notes on and offs), this is known REAPER bug.
            Use `add_note` method instead.

        Parameters
        ----------
        message : Iterable[int]
            Can be any message buffer, for example: (0xb0, 64, 127)
            which is CC64 val127 on channel 1
        position : float
            position at take
        unit : str, optional
            "beats"|"ppq"|"seconds" (default are seconds)
        """
        ...

    def add_fx(self, name: str, even_if_exists: bool = True) -> reapy.FX:
        """
        Add FX to track and return it.

        Parameters
        ----------
        name : str
            FX name.
        even_if_exists : bool, optional
            Whether the FX should be added even if there already is an
            instance of the same FX on the track (default=True).

        Returns
        -------
        fx : FX
            New FX on take (or previously existing instance of FX if
            even_if_exists=False).

        Raises
        ------
        ValueError
            If there is no FX with the specified name.
        """
        ...

    def add_note(self,
                 start: float,
                 end: float,
                 pitch: int,
                 velocity: int = 100,
                 channel: int = 0,
                 selected: bool = False,
                 muted: bool = False,
                 unit: str = "seconds",
                 sort: bool = True) -> None:
        """
        Add MIDI note to take.

        Parameters
        ----------
        start : float
            Note start. Unit depends on ``unit``.
        end : float
            Note end. Unit depends on ``unit``.
        pitch : int
            Note pitch between 0 and 127.
        velocity : int, optional
            Note velocity between 0 and 127 (default=100).
        channel : int, optional
            MIDI channel between 0 and 15.
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool
            Whether to mute new note (default=False).
        unit : {"seconds", "ppq", "beats"}, optional
            Time unit for ``start`` and ``end`` (default="seconds").
            ``"ppq"`` refers to MIDI ticks.
        sort : bool, optional
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.

        See also
        --------
        Take.sort_events
        """
        ...

    def add_sysex(self,
                  message: ty.Iterable[int],
                  position: float,
                  unit: str = "seconds",
                  evt_type: int = -1) -> None:
        """
        Add SysEx event to take.

        Note
        ----
        ⋅ No sort events during this call
        ⋅ No need to add 0xf0 ... 0xf7 bytes (they will be doubled)

        Parameters
        ----------
        message : Iterable[int]
            Can be any message buffer, for example: (0xb0, 64, 127)
            which is CC64 val127 on channel 1
        position : float
            position at take
        unit : str, optional
            "beats"|"ppq"|"seconds" (default are seconds)
        evt_type: int (default -1)
            Allowable types are
            ⋅ -1:sysex (msg should not include bounding F0..F7),
            ⋅ 1-14:MIDI text event types,
            ⋅ 15=REAPER notation event.
        """
        ...

    def beat_to_ppq(self, beat: float) -> float:
        """
        Convert beat number (from project start) to MIDI ticks (of the take).

        Parameters
        ----------
        beat : float
            Beat time to convert in beats.

        Returns
        -------
        ppq : float
            Converted time in MIDI ticks of current take.

        See also
        --------
        Take.ppq_to_beat
        Take.time_to_ppq
        """
        ...

    @property
    def cc_events(self) -> reapy.CCList:
        """
        List of CC events on take.

        :type: CCList
        """
        ...

    @property
    def envelopes(self) -> reapy.EnvelopeList:
        ...

    @property
    def fxs(self) -> reapy.FXList:
        """
        FXs on take.

        :type: FXList
        """
        ...

    def get_info_value(self, param_name: str) -> float:
        ...

    @property
    def has_valid_id(self) ->  bool:
        """
        Whether ReaScript ID is still valid.

        For instance, if take has been deleted, ID will not be valid
        anymore.

        :type: bool
        """

    @property
    def is_active(self) -> bool:
        """
        Whether take is active.

        :type: bool
        """
        ...

    @property
    def is_midi(self) -> bool:
        """
        Whether take contains MIDI or audio.

        :type: bool
        """
        ...

    @property
    def item(self) -> reapy.Item:
        """
        Parent item.

        :type: Item
        """
        ...

    def get_midi(self,
                 size: int = 2*1024*1024) -> ty.List[reapy.MIDIEventDict]:
        """
        Get all midi data of take in one call.

        Parameters
        ----------
        size : int, optional
            predicted size of event buffer to allocate.
            For performance is better to set it to something a but bigger
            than expected buffer size.
            Event with common midi-message (3-bytes) takes 12 bytes.

        Returns
        -------
        List[MIDIEventDict]
            ppq: int
            selected: bool
            muted: bool
            cc_shape: CCShapeFlag
            buf: ty.List[int]

        See also
        --------
        Take.set_midi
        """
        ...

    @property
    def guid(self) -> str:
        """Used for communication within other scripts.

        :type: str
        """
        ...

    def make_active_take(self) -> None:
        """
        Make take active.
        """
        ...

    @property
    def midi_events(self) -> reapy.core.item.midi_event.MIDIEventList[
            reapy.core.item.midi_event.MIDIEvent]:
        """
        Get all midi events as EventList.

        Returns
        -------
        MIDIEventList
        """
        ...

    def midi_hash(self, notes_only: bool = False) -> str:
        """
        Get hash of MIDI-data to compare with later.

        Parameters
        ----------
        notes_only : bool, (False by default)
            count only notes if True

        Returns
        -------
        str
        """
        ...

    def _midi_to_bytestr(self, message: ty.Iterable[int]) -> str: ...

    @property
    def n_cc(self) -> int:
        """
        Number of MIDI CC events in take (always 0 for audio takes).

        :type: int
        """
        ...

    @property
    def n_envelopes(self) -> int:
        """
        Number of envelopes on take.

        :type: int
        """
        ...

    @property
    def n_fxs(self) -> int:
        """
        Number of FXs on take.

        :type: int
        """
        ...

    @property
    def n_midi_events(self) -> int:
        """
        Number of MIDI events in take.

        :type: int
        """
        ...

    @property
    def n_notes(self) -> int:
        """
        Number of MIDI notes in take (always 0 for audio takes).

        :type: int
        """
        ...

    @property
    def n_text_sysex(self) -> int:
        """
        Number of MIDI text/sysex events in take (0 for audio takes).

        :type: int
        """
        ...

    @property
    def name(self) -> str:
        """
        Take name.

        :type: str
        """
        ...

    @property
    def notes(self) -> reapy.NoteList:
        """
        List of MIDI notes on take.

        Unless ``Take.add_note`` has been called with ``sort=False``,
        notes are time-sorted.

        :type: NoteList
        """
        ...

    def ppq_to_beat(self, ppq: float) -> float:
        """
        Convert time in MIDI ticks to beats.

        Note
        ----
        ticks counted from take's start,
        beats from project's start

        Parameters
        ----------
        ppq : float
            Time to convert in MIDI ticks.

        Returns
        -------
        beat : float
            Converted time in beats.

        See also
        --------
        Take.beat_to_ppq
        Take.ppq_to_time
        """
        ...

    def ppq_to_time(self, ppq: float) -> float:
        """
        Convert time in MIDI ticks to seconds.

        Parameters
        ----------
        ppq : float
            Time to convert in MIDI ticks.

        Returns
        -------
        time : float
            Converted time in seconds.

        See also
        --------
        Take.time_to_ppq
        """
        ...

    @property
    def project(self) -> reapy.Project:
        """
        Take parent project.

        :type: reapy.Project
        """

    def _resolve_midi_unit(self,
                           pos_tuple: ty.Tuple[float, ...],
                           unit: str = "seconds") -> ty.Tuple[float, ...]:
        """Get positions as ppq from tuple of positions of any length.

        Parameters
        ----------
        pos_tuple : Tuple[float]
            tuple of position time in bets, ppq or seconds.
        unit : str, optional
            type of position inside tuple: seconds|beats|ppq

        Returns
        -------
        Tuple[float]
            the same tuple normalized to ppq
        """
        ...

    def select_all_midi_events(self, select: bool = True) -> None:
        """
        Select or unselect all MIDI events.

        Parameters
        ----------
        select : bool
            Whether to select or unselect events.

        See also
        --------
        Take.unselect_all_midi_events
        """
        ...

    def set_info_value(self, param_name: str, value: float) -> bool:
        ...

    def set_midi(self,
                 midi: ty.List[reapy.MIDIEventDict],
                 start: ty.Optional[float] = None,
                 unit: str = "seconds",
                 sort: bool = True) -> None:
        """
        Erase all midi from take and build new one from scratch.

        Parameters
        ----------
        midi : List[MIDIEventDict]
            can be taken with `Take.get_midi()` or build from scratch.
        start : float, optional
            if offset needed (for example, start from a particular time)
        unit : str, optional
            time unit: "seconds"|"beats"|"ppq"
        sort : bool, optional
            if sort is needed after insertion

        Raises
        ------
        NotImplementedError
            currently, gaps between events longer than several hours
            are not supported.

        See also
        --------
        Take.get_midi
        """
        ...

    def sort_events(self) -> None:
        """
        Sort MIDI events on take.

        This is only needed if ``Take.add_note`` was called with
        ``sort=False``.

        Examples
        --------
        The following example creates 100 MIDI notes on take in
        reversed order, with ``sort=False`` for efficiency. Thus,
        ``take.notes`` is not time-sorted. ``take.sort_events`` is
        called afterwards so that ``take.notes`` is time-sorted.

        >>> for i in range(100):
        ...     take.add_note(99 - i, 100 - i, pitch=0, sort=False)
        ...
        >>> take.notes[0].start, take.notes[1].start
        99.0, 98.0
        >>> take.sort_events()
        >>> take.notes[0].start, take.notes[1].start
        0.0, 1.0
        """
        ...

    @property
    def source(self) -> reapy.Source:
        """
        Take source.

        :type: Source
        """
        ...

    @property
    def start_offset(self) -> float:
        """
        Start time of the take relative to start of source file.

        :type: float
        """
        ...

    @property
    def text_sysex_events(self) -> reapy.TextSysexList:
        """
        List of text or SysEx events.

        :type: TextSysexList
        """
        ...

    def time_to_ppq(self, time: float) -> float:
        """
        Convert time in seconds to MIDI ticks.

        Parameters
        ----------
        time : float
            Time to convert in seconds.

        Returns
        -------
        ppq : float
            Converted time in MIDI ticks.

        See also
        --------
        Take.ppq_to_time
        """
        ...

    @property
    def track(self) -> reapy.Track:
        """
        Parent track of take.

        :type: Track
        """
        ...

    def unselect_all_midi_events(self) -> None:
        """
        Unselect all MIDI events.

        See also
        --------
        Take.select_all_midi_events
        """
        ...

    @property
    def visible_fx(self) -> ty.Optional[reapy.FX]:
        """
        Visible FX in FX chain if any, else None.

        :type: FX or NoneType
        """
        ...
