import struct
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

    def get_info_value(self, param_name):
        return RPR.GetMediaItemTakeInfo_Value(self.id, param_name)

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

    @reapy.inside_reaper()
    def get_midi(self, size=2*1024*1024):
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
        _, _, buf, buf_size = RPR.MIDI_GetAllEvts(self.id, '', size)
        msg = buf.encode('latin-1')
        out = []
        i = 0
        ppq = 0
        length = len(msg)
        while i < length:
            if length - i < 9:
                break
            ofst, flag, len_ = (
                struct.unpack('<I', msg[i:i + 4])[0], int(msg[i + 4]),
                struct.unpack('<I', msg[i + 5:i + 9])[0]
            )
            ppq += ofst
            buf_b = msg[i + 9:i + 9 + len_]
            buf = [int(b) for b in buf_b]
            i += 9 + len_
            if len_ == 0:
                i += 1
                continue
            out.append(reapy.MIDIEventDict(
                ppq=ppq,
                selected=bool(flag & 1),
                muted=bool(flag & 2),
                cc_shape=reapy.CCShapeFlag(flag & 0b11110000),
                buf=buf
            )
            )
        return out

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
        return reapy.MIDIEventList(self)

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
        return RPR.MIDI_CountEvts(self.id, 1, 1, 1)[0]

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
        Convert time in MIDI ticks to beats.

        Note
        ----
        Ticks are counted from take start, beats — from project start.

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
        # item_start_seconds = self.item.position

        def resolver(pos):
            if unit == "beats":
                return self.beat_to_ppq(pos)
            if unit == "seconds":
                return self.time_to_ppq(pos)
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
    def set_midi(self, midi, start=None, unit="seconds", sort=True):
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
        out = b''
        start_ppq = 0
        if start is not None:
            start_ppq = self._resolve_midi_unit((start,), unit)[0]
        last_ppq = 0 - start_ppq
        for msg in midi:
            evt = b''
            ofst_i = msg['ppq'] - last_ppq
            if ofst_i > 4294967295:
                raise NotImplementedError(
                    'ofset larger than 4294967295 currently not supported'
                )
                # something done with big offset
                # it is about many-many-many hours between events
                # (1 hour is about 8000000 ppq in 120 bpm)
            ofst = struct.pack('<I', int(ofst_i))
            evt += ofst
            last_ppq = msg['ppq']

            flag = bytes(
                [
                    int(msg['selected']) | (int(msg['muted']) << 1)
                    | msg['cc_shape']
                ]
            )
            evt += flag

            len_ = struct.pack('<I', len(msg['buf']))
            evt += len_

            buf = bytes(msg['buf'])
            evt += buf
            out += evt
        packed = out.decode('latin-1')
        RPR.MIDI_SetAllEvts(self.id, packed, len(packed))
        if sort:
            self.sort_events()

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

    @property
    def text_sysex_events(self):
        """
        List of text or SysEx events.

        :type: TextSysexList
        """
        return reapy.TextSysexList(self)

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
