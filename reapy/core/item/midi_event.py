import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList


class MIDIEvent(ReapyObject):

    """Abstract class for MIDI events."""

    def __init__(self, parent, index):
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
        self.index = index
        self.parent = parent

    @property
    def _args(self):
        return self.parent, self.index

    @property
    def _del_name(self):
        return 'MIDI_DeleteEvt'

    def delete(self):
        """Delete event from the take."""
        f = getattr(RPR, self._del_name)
        f(self.parent.id, self.index)

    @reapy.inside_reaper()
    def set(self, message=None, position=None, selected=None,
            muted=None, unit="seconds", sort=True):
        """
        Set properties of event if needed.

        Parameters
        ----------
        message : Iterable[int], optional
            Can be any message buffer, for example: (0xb0, 64, 127)
            which is CC64 val127 on channel 1
        position : float, optional
            position at take
        selected : bool, optional
            Whether to select new note (default=False).
        muted : bool, optional
            Whether to mute new note (default=False).
        unit : str ("seconds as default")
            "beats"|"ppq"|"seconds" (default are seconds)
        sort : bool (True as default)
            Whether to resort notes after creating new note
            (default=True). If False, then the new note will be
            ``take.notes[-1]``. Otherwise it will be at its place in
            the time-sorted list ``take.notes``. Set to False for
            improved efficiency when adding several notes, then call
            ``Take.sort_events`` at the end.
        """
        take = self.parent
        if position:
            position = take._resolve_midi_unit((position,), unit)[0]
        if message:
            message = take._midi_to_bytestr(message)
        RPR.MIDI_SetEvt(take.id, self.index, selected, muted, position,
                        message, len(message), not sort)


class MIDIEventList(ReapyObjectList):

    def __init__(self, parent):
        """
        Create event list.

        Parameters
        ----------
        parent : Take
            Take to which the event list belongs.
        """
        self.parent = parent

    def __getitem__(self, key):
        with reapy.inside_reaper():
            if key >= len(self):
                raise IndexError
            return self._elements_class(self.parent, key)

    def __len__(self):
        return getattr(self.parent, self._n_elements)

    @property
    def _args(self):
        return self.parent,

    @property
    def _elements_class(self):
        return MIDIEvent

    @property
    def _n_elements(self):
        return 'n_midi_events'


class CC(MIDIEvent):

    """MIDI CC event."""

    @property
    def channel(self):
        """
        CC channel between 0 and 15.

        :type: int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[7]

    @property
    def channel_message(self):
        """
        CC channel message.

        :type: int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[6]

    @property
    def _del_name(self):
        return 'MIDI_DeleteCC'

    @reapy.inside_reaper()
    @property
    def infos(self):
        """
        Return infos about CC.

        Keys are {"selected", "muted", "position", "channel",
        "channel_message", "messages"}.

        :type: dict
        """
        res = list(RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        ))[3:]
        res[0] = bool(res[0])
        res[1] = bool(res[1])
        res[2] = self.parent.ppq_to_time(res[2])
        res[-2] = res[-2], res[-1]
        res.pop()
        keys = (
            "selected", "muted", "position", "channel_message", "channel",
            "messages"
        )
        return {k: r for k, r in zip(keys, res)}

    @property
    def messages(self):
        """
        CC messages.

        :type: 2-list of int

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[-2:]

    @property
    def muted(self):
        """
        Whether CC is muted.

        :type: bool

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return bool(RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[4])

    @property
    def position(self):
        """
        CC position in seconds.

        :type: float

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return self.infos["position"]

    @property
    def selected(self):
        """
        Whether CC is selected.

        :type: bool

        See also
        --------
        CC.infos
            For maximum efficiency when querying several properties of
            a CC.
        """
        return bool(RPR.MIDI_GetCC(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[3])


class CCList(MIDIEventList):

    _elements_class = CC
    _n_elements = "n_cc"


class Note(MIDIEvent):

    """MIDI note."""

    @property
    def channel(self):
        """
        Note channel between 0 and 15.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[7]

    @property
    def _del_name(self):
        return 'MIDI_DeleteNote'

    @property
    def end(self):
        """
        Note end in seconds.

        :type: float

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return self.infos["end"]

    @property
    def infos(self):
        """
        Return infos about note.

        Keys are {"selected", "muted", "start", "end", "channel",
        "pitch", "velocity"}.

        :type: dict
        """
        res = list(RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        ))[3:]
        res[0] = bool(res[0])
        res[1] = bool(res[1])
        res[2] = self.parent.ppq_to_time(res[2])
        res[3] = self.parent.ppq_to_time(res[3])
        keys = (
            "selected", "muted", "start", "end", "channel", "pitch",
            "velocity"
        )
        return {k: r for k, r in zip(keys, res)}

    @property
    def muted(self):
        """
        Whether note is muted.

        :type: bool

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return bool(RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[4])

    @property
    def pitch(self):
        """
        Note pitch between 0 and 127.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[8]

    @property
    def selected(self):
        """
        Whether note is selected.

        :type: bool

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return bool(RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[3])

    @property
    def start(self):
        """
        Note start in seconds.

        :type: float

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return self.infos["start"]

    @property
    def velocity(self):
        """
        Note velocity between 0 and 127.

        :type: int

        See also
        --------
        Note.infos
            For maximum efficiency when querying several properties of
            a Note.
        """
        return RPR.MIDI_GetNote(
            self.parent.id, self.index, 0, 0, 0, 0, 0, 0, 0
        )[9]


class NoteList(MIDIEventList):

    _elements_class = Note
    _n_elements = "n_notes"
