import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.tools import Program


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
        raise NotImplementedError

    @property
    def _n_elements(self):
        raise NotImplementedError


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
    def infos(self):
        """
        Return infos about CC.

        Keys are {"selected", "muted", "position", "channel",
        "channel_message", "messages"}.

        :type: dict
        """
        code = """
        res = list(RPR.MIDI_GetCC(
            take.id, index, 0, 0, 0, 0, 0, 0, 0
        ))[3:]
        res[0] = bool(res[0])
        res[1] = bool(res[1])
        res[2] = take.ppq_to_time(res[2])
        res[-2] = res[-2], res[-1]
        res.pop()
        keys = (
            "selected", "muted", "position", "channel_message", "channel",
            "messages"
        )
        infos = {k: r for k, r in zip(keys, res)}
        """
        infos, = Program(code, "infos").run(
            take=self.parent, index=self.index
        )
        return infos

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
        code = """
        res = list(RPR.MIDI_GetNote(
            take.id, index, 0, 0, 0, 0, 0, 0, 0
        ))[3:]
        res[0] = bool(res[0])
        res[1] = bool(res[1])
        res[2] = take.ppq_to_time(res[2])
        res[3] = take.ppq_to_time(res[3])
        keys = (
            "selected", "muted", "start", "end", "channel", "pitch",
            "velocity"
        )
        infos = {k: r for k, r in zip(keys, res)}
        """
        infos, = Program(code, "infos").run(
            take=self.parent, index=self.index
        )
        return infos

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
