import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import InvalidObjectError, UndefinedEnvelopeError


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

    >>> reapy.Track("PIANO", project)
    Track("(MediaTrack*)0x00000000110A1AD0")
    """

    def __init__(self, id, project=None):
        self._project = None
        if isinstance(id, int):  # id is a track index
            id = RPR.GetTrack(project.id, id)
            if id.endswith("0x0000000000000000"):
                raise IndexError('Track index out of range')
            self._project = project
        elif isinstance(id, str) and not id.startswith("(MediaTrack*)"):
            # id is a track name
            name = id
            id = project._get_track_by_name(name).id
            if id.endswith("0x0000000000000000"):
                raise KeyError(name)
            self._project = project
        # id is now a real ReaScript ID
        self.id = id

    @property
    def _args(self):
        return self.id,

    @classmethod
    def _get_id_from_pointer(cls, pointer):
        return '(MediaTrack*)0x{0:0{1}X}'.format(int(pointer), 16)

    @reapy.inside_reaper()
    def _get_project(self):
        """
        Return parent project of track.

        Should only be used internally; one should directly access
        Track.project instead of calling this method.
        """
        for project in reapy.get_projects():
            if self.id in [t.id for t in project.tracks]:
                return project

    def add_audio_accessor(self):
        """
        Create audio accessor and return it.

        Returns
        -------
        audio_accessor : AudioAccessor
            Audio accessor on track.
        """
        audio_accessor_id = RPR.CreateTrackAudioAccessor(self.id)
        audio_accessor = reapy.AudioAccessor(audio_accessor_id)
        return audio_accessor

    def add_fx(self, name, input_fx=False, even_if_exists=True):
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
        index = RPR.TrackFX_AddByName(
            self.id, name, input_fx, 1 - 2 * even_if_exists
        )
        if index == -1:
            raise ValueError("Can't find FX named {}".format(name))
        fx = reapy.FX(self, index)
        return fx

    @reapy.inside_reaper()
    def add_item(self, start=0, end=None, length=0):
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
        if end is None:
            end = start + length
        item = reapy.Item(RPR.AddMediaItemToTrack(self.id))
        item.position = start
        item.length = end - start
        return item

    def add_midi_item(self, start=0, end=1, quantize=False):
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
        item_id = RPR.CreateNewMIDIItemInProj(self.id, start, end, quantize)[0]
        item = reapy.Item(item_id)
        return item

    def add_send(self, destination=None):
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
        if isinstance(destination, Track):
            destination = destination.id
        send_id = RPR.CreateTrackSend(self.id, destination)
        type = "hardware" if destination is None else "send"
        send = reapy.Send(self, send_id, type=type)
        return send

    @property
    def automation_mode(self):
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
        modes = "trim/read", "read", "touch", "write", "latch", "latch preview"
        automation_mode = modes[RPR.GetTrackAutomationMode(self.id)]
        return automation_mode

    @automation_mode.setter
    def automation_mode(self, mode):
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
        modes = "trim/read", "read", "touch", "write", "latch", "latch preview"
        RPR.SetTrackAutomationMode(self.id, modes.index(mode))

    @property
    def color(self):
        """
        Track color in RGB format.

        :type: tuple of int
        """
        native_color = RPR.GetTrackColor(self.id)
        r, g, b = reapy.rgb_from_native(native_color)
        return r, g, b

    @color.setter
    def color(self, color):
        """
        Set track color to `color`

        Parameters
        ----------
        color : tuple
            Triplet of integers between 0 and 255 corresponding to RGB
            values.
        """
        native_color = reapy.rgb_to_native(color)
        RPR.SetTrackColor(self.id, native_color)

    def delete(self):
        """
        Delete track.
        """
        RPR.DeleteTrack(self.id)

    @property
    def depth(self):
        """
        Track depth.

        :type: int
        """
        depth = RPR.GetTrackDepth(self.id)
        return depth

    @property
    def envelopes(self):
        """
        List of envelopes on track.

        :type: EnvelopeList
        """
        return reapy.EnvelopeList(self)

    @property
    def fxs(self):
        """
        List of FXs on track.

        :type: FXList
        """
        fxs = reapy.FXList(self)
        return fxs

    def get_info_string(self, param_name):
        return RPR.GetSetMediaTrackInfo_String(self.id, param_name, "", False)[3]

    def get_info_value(self, param_name):
        value = RPR.GetMediaTrackInfo_Value(self.id, param_name)
        return value

    @property
    def GUID(self):
        """
        Track's GUID.

        16-byte GUID, can query or update.
        If using a _String() function, GUID is a string {xyz-...}.

        :type: str
        """
        return RPR.GetTrackGUID(self.id)

    @GUID.setter
    def GUID(self, guid_string):
        self.set_info_string("GUID", guid_string)

    @reapy.inside_reaper()
    @property
    def has_valid_id(self):
        """
        Whether ReaScript ID is still valid.

        For instance, if track has been deleted, ID will not be valid
        anymore.

        :type: bool
        """
        pointer, name = self._get_pointer_and_name()
        if self._project is None:
            return any(
                RPR.ValidatePtr2(p.id, pointer, name)
                for p in reapy.get_projects()
            )
        return bool(RPR.ValidatePtr2(self.project.id, pointer, name))

    @property
    def icon(self):
        """
        Track icon.

        Full filename, or relative to resource_path/data/track_icons.

        :type: str
        """
        return self.get_info_string("P_ICON")

    @icon.setter
    def icon(self, filename):
        self.set_info_string("P_ICON", filename)

    @property
    def index(self):
        """Track index in GUI (0-based).

        Will be ``None`` for master track.

        :type: int or None

        Raises
        ------
        InvalidObjectError
            When track does not exist in REAPER.
        """
        index = int(self.get_info_value('IP_TRACKNUMBER')) - 1
        if index >= 0:
            return index
        if index == -1:
            raise InvalidObjectError(self)

    @property
    def instrument(self):
        """
        First instrument FX on track if it exists, else None.

        :type: FX or None
        """
        fx_index = RPR.TrackFX_GetInstrument(self.id)
        instrument = None if fx_index == -1 else reapy.FX(self, fx_index)
        return instrument

    @reapy.inside_reaper()
    @property
    def items(self):
        """
        List of items on track.

        :type: list of Item
        """
        n_items = RPR.CountTrackMediaItems(self.id)
        item_ids = [
            RPR.GetTrackMediaItem(self.id, i) for i in range(n_items)
        ]
        return list(map(reapy.Item, item_ids))

    @property
    def is_muted(self):
        """
        Whether track is muted.

        Can be manually set to change track state.
        """
        return bool(self.get_info_value("B_MUTE"))

    @is_muted.setter
    def is_muted(self, muted):
        if muted:
            self.mute()
        else:
            self.unmute()

    @property
    def is_selected(self):
        """
        Whether track is selected.

        :type: bool
        """
        is_selected = bool(RPR.IsTrackSelected(self.id))
        return is_selected

    @is_selected.setter
    def is_selected(self, selected):
        """
        Select or unselect track.

        Parameters
        ----------
        selected : bool
            Whether to select or unselect track.
        """
        if selected:
            self.select()
        else:
            self.unselect()

    @property
    def is_solo(self):
        """
        Whether track is solo.

        Can be manually set to change track state.
        """
        return bool(self.get_info_value("I_SOLO"))

    @is_solo.setter
    def is_solo(self, solo):
        if solo:
            self.solo()
        else:
            self.unsolo()

    def make_only_selected_track(self):
        """
        Make track the only selected track in parent project.
        """
        RPR.SetOnlyTrackSelected(self.id)

    def midi_hash(self, notes_only=False):
        """Get hash of MIDI-data to compare with later.

        Parameters
        ----------
        notes_only : bool, (False by default)
            count only notes if True

        Returns
        -------
        str
        """
        return RPR.MIDI_GetTrackHash(self.id, notes_only, 'hash', 1024**2)[3]

    @property
    def midi_note_names(self):
        with reapy.inside_reaper():
            names = [
                RPR.GetTrackMIDINoteName(self.id, i, 0) for i in range(128)
            ]
        return names

    @reapy.inside_reaper()
    def mute(self):
        """Mute track (do nothing if track is already muted)."""
        if not self.is_muted:
            self.toggle_mute()

    @property
    def n_envelopes(self):
        """
        Number of envelopes on track.

        :type: int
        """
        n_envelopes = RPR.CountTrackEnvelopes(self.id)
        return n_envelopes

    @property
    def n_fxs(self):
        """
        Number of FXs on track.

        :type: int
        """
        n_fxs = RPR.TrackFX_GetCount(self.id)
        return n_fxs

    @property
    def n_hardware_sends(self):
        """
        Number of hardware sends on track.

        :type: int
        """
        n_hardware_sends = RPR.GetTrackNumSends(self.id, 1)
        return n_hardware_sends

    @property
    def n_items(self):
        """
        Number of items on track.

        :type: int
        """
        n_items = RPR.CountTrackMediaItems(self.id)
        return n_items

    @property
    def n_receives(self):
        n_receives = RPR.GetTrackNumSends(self.id, -1)
        return n_receives

    @property
    def n_sends(self):
        n_sends = RPR.GetTrackNumSends(self.id, 0)
        return n_sends

    @property
    def name(self):
        """
        Track name.

        Name is "MASTER" for master track, "Track N" if track has no
        name.

        :type: str
            Track name .
        """
        _, _, name, _ = RPR.GetTrackName(self.id, "", 2048)
        return name

    @name.setter
    def name(self, track_name):
        self.set_info_string("P_NAME", track_name)

    @property
    def parent_track(self):
        """
        Parent track, or None if track has none.

        :type: Track or NoneType
        """
        parent = Track(RPR.GetParentTrack(self.id))
        if not parent._is_defined:
            parent = None
        return parent

    @property
    def project(self):
        """
        Track parent project.

        :type: Project
        """
        if self._project is None:
            self._project = self._get_project()
        return self._project

    @reapy.inside_reaper()
    @property
    def receives(self):
        return [
            reapy.Send(self, i, type="receive") for i in range(self.n_receives)
        ]

    def select(self):
        """
        Select track.
        """
        RPR.SetTrackSelected(self.id, True)

    @reapy.inside_reaper()
    @property
    def sends(self):
        return [
            reapy.Send(self, i, type="send") for i in range(self.n_sends)
        ]

    def set_info_string(self, param_name, param_string):
        RPR.GetSetMediaTrackInfo_String(
            self.id, param_name, param_string, True)

    def set_info_value(self, param_name, param_value):
        RPR.SetMediaTrackInfo_Value(self.id, param_name, param_value)

    @reapy.inside_reaper()
    def solo(self):
        """Solo track (do nothing if track is already solo)."""
        if not self.is_solo:
            self.toggle_solo()

    @reapy.inside_reaper()
    def toggle_mute(self):
        """Toggle mute on track."""
        selected_tracks = self.project.selected_tracks
        self.make_only_selected_track()
        self.project.perform_action(40280)
        self.project.selected_tracks = selected_tracks

    @reapy.inside_reaper()
    def toggle_solo(self):
        """Toggle solo on track."""
        selected_tracks = self.project.selected_tracks
        self.make_only_selected_track()
        self.project.perform_action(7)
        self.project.selected_tracks = selected_tracks

    @reapy.inside_reaper()
    def unmute(self):
        """Unmute track (do nothing if track is not muted)."""
        if self.is_muted:
            self.toggle_mute()

    def unselect(self):
        """
        Unselect track.
        """
        RPR.SetTrackSelected(self.id, False)

    @reapy.inside_reaper()
    def unsolo(self):
        """Unsolo track (do nothing if track is not solo)."""
        if self.is_solo:
            self.toggle_solo()

    @property
    def visible_fx(self):
        """
        Visible FX in FX chain if any, else None.

        :type: FX or NoneType
        """
        with reapy.inside_reaper():
            return self.fxs[RPR.TrackFX_GetChainVisible(self.id)]


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

    def __init__(self, parent):
        """
        Create track list.

        Parameters
        ----------
        parent : Project
            Parent project.
        """
        self.parent = parent

    @reapy.inside_reaper()
    def __delitem__(self, key):
        tracks = self[key] if isinstance(key, slice) else [self[key]]
        for track in tracks:
            track.delete()

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._get_items_from_slice(key)
        return Track(key, self.parent)

    def __iter__(self):
        tracks = self[:]  # Only cost one distant call
        for track in tracks:
            yield track

    def __len__(self):
        return self.parent.n_tracks

    @property
    def _args(self):
        return self.parent,

    @reapy.inside_reaper()
    def _get_items_from_slice(self, slice):
        indices = range(*slice.indices(len(self)))
        return [self[i] for i in indices]
