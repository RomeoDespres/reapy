import struct
import warnings

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Take(ReapyObject):

    _class_name = "Take"

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, Take) and self.id == other.id

    @property
    def _args(self):
        return self.id,

    def add_audio_accessor(self):
        """
        Create audio accessor and return it.

        Returns
        -------
        audio_accessor : AudioAccessor
            Audio accessor on take.
        """
        audio_accessor_id = RPR.CreateTakeAudioAccessor(self.id)
        audio_accessor = reapy.AudioAccessor(audio_accessor_id)
        return audio_accessor

    @reapy.inside_reaper()
    def add_event(self, message, position, unit="seconds"):
        """
        Add generic event to the take at position.

        Note
        ----
        ⋅ No sort events during this call
        ⋅ Inserting notes within this function causes problems
            (wrong note on and off timing), this is known REAPER bug.
            Use `Take.add_note` instead.

        Parameters
        ----------
        message : Iterable[int]
            Can be any message buffer, for example: (0xb0, 64, 127)
            which is CC64 val127 on channel 1
        position : float
            position at take
        unit : str, optional
            "beats"|"ppq"|"seconds" (default are seconds)

        See also
        --------
        Take.add_note
        """
        ppqpos = self._resolve_midi_unit((position,), unit)[0]
        bytestr = self._midi_to_bytestr(message)
        RPR.MIDI_InsertEvt(
            self.id, False, False, ppqpos, bytestr, len(bytestr)
        )

    def add_fx(self, name, even_if_exists=True):
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
        index = RPR.TakeFX_AddByName(
            self.id, name, 1 - 2*even_if_exists
        )
        if index == -1:
            raise ValueError("Can't find FX named {}".format(name))
        fx = reapy.FX(self, index)
        return fx

    @reapy.inside_reaper()
    def add_note(
        self, start, end, pitch, velocity=100, channel=0, selected=False,
        muted=False, unit="seconds", sort=True
    ):
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
        start, end = self._resolve_midi_unit((start, end), unit)
        sort = bool(not sort)
        args = (
            self.id, selected, muted, start, end, channel, pitch, velocity,
            sort
        )
        RPR.MIDI_InsertNote(*args)

    @reapy.inside_reaper()
    def add_sysex(self, message, position, unit="seconds", evt_type=-1):
        """
        Add SysEx event to take.

        Notes
        -----
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
        bytestr = self._midi_to_bytestr(message)
        ppqpos = self._resolve_midi_unit((position,), unit)[0]
        RPR.MIDI_InsertTextSysexEvt(
            self.id, False, False, ppqpos, evt_type, bytestr, len(bytestr)
        )

    def beat_to_ppq(self, beat):
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
        ppq = RPR.MIDI_GetPPQPosFromProjQN(self.id, beat)
        return ppq

    @property
    def cc_events(self):
        """
        List of CC events on take.

        :type: CCList
        """
        return reapy.CCList(self)

    @reapy.inside_reaper()
    def delete_midi_event(self, index):
        """Delete MIDI event by index.

        Parameters
        ----------
        index : int
            MIDI event index in take. May be negative.
        """
        index = list(range(self.n_midi_events))[index]
        RPR.MIDI_DeleteEvt(self.id, index)

    @property
    def envelopes(self):
        return reapy.EnvelopeList(self)

    @property
    def fxs(self):
        """
        FXs on take.

        :type: FXList
        """
        return reapy.FXList(self)

    @reapy.inside_reaper()
    def get_first_selected_event_index(self, after=None):
        """Return index of first selected MIDI event after index.

        Return value is ``None`` if no such event exists.

        Parameters
        ----------
        after : int, optional
            If specified, the first selected MIDI event index that is
            strictly higher than ``after`` will be returned
            (default=``None``). May be negative.

        Returns
        -------
        int or None
            First selected MIDI event index after ``after``. Defaults
            to ``None`` if no such event exists.
        """
        after = -1 if after is None else list(range(self.n_midi_events))[after]
        index = RPR.MIDI_EnumSelEvts(self.id, after)
        if index != -1:
            return index

    def get_info_value(self, param_name):
        return RPR.GetMediaItemTakeInfo_Value(self.id, param_name)

    @reapy.inside_reaper()
    def get_midi_event(self, index):
        """Return information about a specific MIDI event.

        Parameters
        ----------
        index : int
            MIDI event index in take. May be negative.

        Returns
        -------
        dict
            MIDI event data with keys ``message``, ``muted``,
            ``ppq_position`` (counted from take start) and
            ``selected``.
        """
        index = list(range(self.n_midi_events))[index]
        max_length = length = 2**8
        while length == max_length or length == 0:
            max_length *= 2
            result = RPR.MIDI_GetEvt(
                self.id, index, False, False, 0, "", max_length
            )
            success, _, _, selected, muted, ppq_position, msg, length = result
        if not success:
            raise RuntimeError("Couldn't retrieve event data.")
        return {
            "message": list(msg.encode("latin-1")),
            "muted": bool(muted),
            "ppq_position": ppq_position,
            "selected": bool(selected),
        }

    @reapy.inside_reaper()
    def get_midi_events(self):
        """Return list of all MIDI events on take.

        Returns
        -------
        list of dict
            List of MIDI events data. Each event is represented by a
            dict with keys ``message``, ``muted``, ``ppq_position``
            (counted from take start) and ``selected``. Control
            change, channel pressure, and pitch events have an
            additional ``shape`` key. Events with ``shape == 'bezier'``
            also have a ``bezier_tension`` key.

        See also
        --------
        Take.get_midi_event
        Take.set_midi_event
        Take.set_midi_events
        """
        class MIDIEvents:

            shapes = {
                0b0000000: "square",
                0b0010000: "linear",
                0b0100000: "slow start/end",
                0b0110000: "fast start",
                0b1000000: "fast end",
                0b1010000: "bezier"
            }

            def __iter__(self):
                self.it = iter(data.encode("latin1"))
                self.ppq_position = 0
                return self

            def __next__(self):
                self.ppq_position += struct.unpack("<I", self.read(4))[0]
                flag = self.read(1)[0]
                message_length = struct.unpack("<I", self.read(4))[0]
                if message_length == 0:
                    return next(self)
                event = {
                    "message": list(self.read(message_length)),
                    "muted": bool(flag & 2),
                    "ppq_position": self.ppq_position,
                    "selected": bool(flag & 1)
                }
                status = event["message"][0]
                if 0xb0 <= status <= 0xbf or 0xd0 <= status <= 0xef:
                    # Message is control change, aftertouch or pitch
                    event["shape"] = self.shapes[flag & 0b1110000]
                    if event["shape"] == "bezier":  # Also get Bezier shape
                        bezier_tension = bytes(next(self)["message"][-4:])
                        bezier_tension = struct.unpack("f", bezier_tension)[0]
                        event["bezier_tension"] = bezier_tension
                return event

            def read(self, n):
                return bytes([next(self.it) for _ in range(n)])

        max_length = length = 2**12
        while length == max_length:
            max_length *= 2
            success, _,  data, length = RPR.MIDI_GetAllEvts(
                self.id, "", max_length
            )
        if success:
            # Return all events except last one which is an automatically
            # inserted "all notes off" that can not be retrieved with
            # get_midi_event(-1).
            return list(MIDIEvents())[:-1]
        else:
            raise RuntimeError("Couldn't retrieve take data.")

    @reapy.inside_reaper()
    @property
    def has_valid_id(self):
        """
        Whether ReaScript ID is still valid.

        For instance, if take has been deleted, ID will not be valid
        anymore.

        :type: bool
        """
        try:
            project_id = self.track.project.id
        except (OSError, AttributeError):
            return False
        pointer, name = self._get_pointer_and_name()
        return bool(RPR.ValidatePtr2(project_id, pointer, name))

    @reapy.inside_reaper()
    @property
    def is_active(self):
        """
        Whether take is active.

        :type: bool
        """
        return self == self.item.active_take

    @property
    def is_midi(self):
        """
        Whether take contains MIDI or audio.

        :type: bool
        """
        return bool(RPR.TakeIsMIDI(self.id))

    @property
    def item(self):
        """
        Parent item.

        :type: Item
        """
        return reapy.Item(RPR.GetMediaItemTake_Item(self.id))

    @property
    def guid(self):
        """
        Used for communication within other scripts.

        :type: str
        """
        _, _, _, guid, _ = RPR.GetSetMediaItemTakeInfo_String(
            self.id, 'GUID', 'stringNeedBig', False
        )
        return guid

    def make_active_take(self):
        """
        Make take active.
        """
        RPR.SetActiveTake(self.id)

    @property
    def midi_events(self):
        """
        Get all midi events as EventList.

        Returns
        -------
        MIDIEventList
        """
        deprecation_message = (
            "Take.midi_events is deprecated in favor of "
            "Take.get_midi_event(). Use the latter instead."
        )
        warnings.warn(FutureWarning(deprecation_message))
        return reapy.core.item.midi_event.MIDIEventList(self)

    @property
    def midi_grid(self):
        """
        Return most recent MIDI editor grid properties for this take.

        Returns
        -------
        size : float
            Grid size in quarter notes.
        swing : float
            Grid swing from 0 to 1.
        note_length : float or None
            Note length in quarter notes. Defaults to None when set to
            match grid.
        """
        size, _, swing, note_length = RPR.MIDI_GetGrid(self.id, 0, 0)
        if note_length == 0:
            note_length = None
        return size, swing, note_length

    def midi_hash(self, notes_only=False):
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
        return RPR.MIDI_GetHash(self.id, notes_only, 'hash', 1024**2)[3]

    def _midi_to_bytestr(self, message):
        return bytes(message).decode('latin-1')

    @property
    def n_cc(self):
        """
        Number of MIDI CC events in take (always 0 for audio takes).

        :type: int
        """
        return RPR.MIDI_CountEvts(self.id, 0, 0, 0)[3]

    @property
    def n_envelopes(self):
        """
        Number of envelopes on take.

        :type: int
        """
        return RPR.CountTakeEnvelopes(self.id)

    @property
    def n_fxs(self):
        """
        Number of FXs on take.

        :type: int
        """
        return RPR.TakeFX_GetCount(self.id)

    @property
    def n_midi_events(self):
        """
        Number of MIDI events in take.

        :type: int
        """
        n_notes, n_cc, n_text_sysex = RPR.MIDI_CountEvts(self.id, 1, 1, 1)[2:]
        return 2*n_notes + n_cc + n_text_sysex

    @property
    def n_notes(self):
        """
        Number of MIDI notes in take (always 0 for audio takes).

        :type: int
        """
        return RPR.MIDI_CountEvts(self.id, 0, 0, 0)[2]

    @property
    def n_text_sysex(self):
        """
        Number of MIDI text/sysex events in take (0 for audio takes).

        :type: int
        """
        return RPR.MIDI_CountEvts(self.id, 0, 0, 0)[4]

    @property
    def name(self):
        """
        Take name.

        :type: str
        """
        if self._is_defined:
            return RPR.GetTakeName(self.id)
        return ""

    @property
    def notes(self):
        """
        List of MIDI notes on take.

        Unless ``Take.add_note`` has been called with ``sort=False``,
        notes are time-sorted.

        :type: NoteList
        """
        return reapy.NoteList(self)

    def ppq_to_beat(self, ppq):
        """
        Convert time in MIDI ticks (from take's start) to beats (from project's start).

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
        beat = RPR.MIDI_GetProjQNFromPPQPos(self.id, ppq)
        return beat

    def ppq_to_time(self, ppq):
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
        time = RPR.MIDI_GetProjTimeFromPPQPos(self.id, ppq)
        return time

    @reapy.inside_reaper()
    @property
    def project(self):
        """
        Take parent project.

        :type: reapy.Project
        """
        return self.item.project

    @reapy.inside_reaper()
    def _resolve_midi_unit(self, pos_tuple, unit="seconds"):
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
        if unit == "ppq":
            return pos_tuple
        item_start_seconds = self.item.position

        def resolver(pos):
            if unit == "beats":
                take_start_beat = self.track.project.time_to_beats(
                    item_start_seconds
                )
                return self.beat_to_ppq(take_start_beat + pos)
            if unit == "seconds":
                return self.time_to_ppq(item_start_seconds + pos)
            raise ValueError('unit param should be one of seconds|beats|ppq')
        return [resolver(pos) for pos in pos_tuple]

    def select_all_midi_events(self, select=True):
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
        RPR.MIDI_SelectAll(self.id, select)

    def set_info_value(self, param_name, value):
        return RPR.SetMediaItemTakeInfo_Value(self.id, param_name, value)

    @reapy.inside_reaper()
    def set_midi_event(
        self, index, message=None, muted=None, ppq_position=None,
        selected=None, sort=True
    ):
        """Set MIDI event information.

        Parameters that are unspecified or set to ``None`` will not
        be modified.

        Parameters
        ----------
        index : int
            MIDI event index in take. May be negative.
        message : list of int, bytes or str (optional)
            New MIDI message. The preferred input type is list of int.
            Strings should be the Latin-1 encoding of the byte
            sequence.
        muted : bool, optional
            Whether to mute event.
        ppq_position : float, optional
            New PPQ position counted from take start.
        selected : bool, optional
            Whether to select event.
        sort : bool, optional
            Whether to sort take events after setting data
            (default=``True``). When ``True`` and ``ppq_position``
            is not ``None``, event index is likely to change. When
            calling ``Take.set_midi_event`` several times in a row,
            performance may be improved by setting it to ``False``.
            However, users should make sure to sort events afterwards
            because unsorted events may cause bugs.
        """
        index = list(range(self.n_midi_events))[index]
        if isinstance(message, list):
            message = bytes(message)
        if isinstance(message, bytes):
            message = message.decode("latin1")
        message_size = None if message is None else len(message)
        success = RPR.MIDI_SetEvt(
            self.id, index, selected, muted, ppq_position, message,
            message_size, not sort
        )
        if not success:
            raise RuntimeError("Couldn't set event data.")

    @reapy.inside_reaper()
    def set_midi_events(self, events):
        """Erase and replace all events on take.

        Parameters
        ----------
        events : iterable of dict
            Time-sorted iterable of MIDI events. Each MIDI event is
            represented by a ``dict`` with the following keys:

            - ``ppq_position`` (*int*) – Event position in MIDI ticks,
              counted from take start.
            - ``message`` (*list of int*) – Event MIDI message.
            - ``muted`` (*bool, optional*) – Whether event is muted.
              Default is ``False``.
            - ``selected`` (*bool, optional*) – Wether event is
              selected. Default is ``False``.
            - ``shape`` (*{'square', 'linear', 'slow start/end',
              'fast start', 'fast end', 'bezier'}, optional*) – Event
              shape. Will be ignored for events where shape can not be
              set (e.g. MIDI notes). Default is ``square``.
            - ``bezier_tension`` (*float, optional*) – Event shape
              Bezier tension. Will be ignored if ``shape`` is not
              ``bezier``. Default is ``0``.

        Raises
        ------
        ValueError
            When ``events`` is not time-sorted or when an event has a
            negative ``ppq_position``.

        See also
        --------
        Take.get_midi_event
        Take.set_midi_event
        Take.get_midi_events
        """
        def generate_bytes(events):
            shapes = {
                "square": 0b0000000,
                "linear": 0b0010000,
                "slow start/end": 0b0100000,
                "fast start": 0b0110000,
                "fast end": 0b1000000,
                "bezier": 0b1010000
            }
            last_ppq_position = 0
            bezier_message = (
                b"\x00\x00\x00\x00\x00\x0c\x00\x00\x00\xc3\xbf\x0fCCBZ "
            )
            for i, event in enumerate(events):
                ppq_position = event["ppq_position"]
                if ppq_position < 0:
                    msg = "Event {} has negative ppq_position={}."
                    raise ValueError(msg.format(i, ppq_position))
                offset = int(event["ppq_position"]) - last_ppq_position
                if offset < 0:
                    msg = (
                        "Input iterable is not time-sorted. Event {} has "
                        "ppq_position={} while event {} has ppq_position={}."
                    )
                    msg = msg.format(i, ppq_position, i - 1, last_ppq_position)
                    raise ValueError(msg)
                last_ppq_position += offset
                while offset >= 2**31:
                    offset -= 2**31 - 1
                    yield from b"\xff\xff\xff\x7f\x00\x00\x00\x00\x00"
                yield from struct.pack("<I", offset)
                flag = 0
                if event.get("selected", False):
                    flag |= 1
                if event.get("muted", False):
                    flag |= 2
                shape = event.get("shape", "square")
                flag |= shapes[shape]
                yield flag
                yield from struct.pack("<I", len(event["message"]))
                yield from event["message"]
                if shape == "bezier":
                    yield from bezier_message
                    yield from struct.pack("f", event.get("bezier_tension", 0))
        item_end = int(self.time_to_ppq(self.item.position + self.item.length))
        all_notes_off = {"ppq_position": item_end, "message": [176, 123, 0]}
        data = bytes(generate_bytes(events + [all_notes_off])).decode("latin1")
        success = RPR.MIDI_SetAllEvts(self.id, data, len(data))
        if not success:
            raise RuntimeError("Couldn't set take data.")
        self.sort_events()  # Fix missing note off events

    def sort_events(self):
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
        RPR.MIDI_Sort(self.id)

    @property
    def source(self):
        """
        Take source.

        :type: Source
        """
        return reapy.Source(RPR.GetMediaItemTake_Source(self.id))

    @property
    def start_offset(self):
        """
        Start time of the take relative to start of source file.

        :type: float
        """
        return self.get_info_value("D_STARTOFFS")

    def time_to_ppq(self, time):
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
        ppq = RPR.MIDI_GetPPQPosFromProjTime(self.id, time)
        return ppq

    @property
    def track(self):
        """
        Parent track of take.

        :type: Track
        """
        track_id = RPR.GetMediaItemTake_Track(self.id)
        return reapy.Track(track_id)

    def unselect_all_midi_events(self):
        """
        Unselect all MIDI events.

        See also
        --------
        Take.select_all_midi_events
        """
        self.select_all_midi_events(select=False)

    @property
    def visible_fx(self):
        """
        Visible FX in FX chain if any, else None.

        :type: FX or NoneType
        """
        with reapy.inside_reaper():
            return self.fxs[RPR.TakeFX_GetChainVisible(self.id)]
