"""Defines class Project."""

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.errors import RedoError, UndoError


class Project(ReapyObject):

    """REAPER project."""

    def __init__(self, id=None, index=-1):
        """
        Build project either by ID or index.

        Parameters
        ----------
        id : str, optional
            Project ID. If None, `index` must be specified.
        index : int, optional
            Project index in GUI (default=-1, corresponds to current
            project).
        """
        if id is None:
            id = RPR.EnumProjects(index, None, 0)[0]
        self.id = id

    def __eq__(self, other):
        if hasattr(other, 'id'):
            return self.id == other.id
        return False

    @property
    def _args(self):
        return self.id,

    @reapy.inside_reaper()
    def _get_track_by_name(self, name):
        """Return first track with matching name."""
        for track in self.tracks:
            if track.name == name:
                return track

    def add_marker(self, position, name="", color=0):
        """
        Create new marker and return its index.

        Parameters
        ----------
        position : float
            Marker position in seconds.
        name : str, optional
            Marker name.
        color : int or tuple of int, optional
            Marker color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.

        Returns
        -------
        marker : reapy.Marker
            New marker.

        Notes
        -----
        If a marker with the same position and name already exists, no
        new marker will be created, and the existing marker index will
        be returned.
        """
        if isinstance(color, tuple):
            color = reapy.rgb_to_native(color) | 0x1000000
        marker_id = RPR.AddProjectMarker2(
            self.id, False, position, 0, name, -1, color
        )
        marker = reapy.Marker(self, marker_id)
        return marker

    def add_region(self, start, end, name="", color=0):
        """
        Create new region and return its index.

        Parameters
        ----------
        start : float
            Region start in seconds.
        end : float
            Region end in seconds.
        name : str, optional
            Region name.
        color : int or tuple of int, optional
            Region color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.

        Returns
        -------
        region : reapy.Region
            New region.
        """
        if isinstance(color, tuple):
            color = reapy.rgb_to_native(color) | 0x1000000
        region_id = RPR.AddProjectMarker2(
            self.id, True, start, end, name, -1, color
        )
        region = reapy.Region(self, region_id)
        return region

    @reapy.inside_reaper()
    def add_track(self, index=0, name=""):
        """
        Add track at a specified index.

        Parameters
        ----------
        index : int
            Index at which to insert track.
        name : str, optional
            Name of created track.

        Returns
        -------
        track : Track
            New track.
        """
        n_tracks = self.n_tracks
        index = max(-n_tracks, min(index, n_tracks))
        if index < 0:
            index = index % n_tracks
        with self.make_current_project():
            RPR.InsertTrackAtIndex(index, True)
        track = self.tracks[index]
        track.name = name
        return track

    @property
    def any_track_solo(self):
        """
        Test whether any track is soloed in project.

        Returns
        -------
        any_track_solo : bool
            Whether any track is soloed in project.
        """
        any_track_solo = bool(RPR.AnyTrackSolo(self.id))
        return any_track_solo

    def beats_to_time(self, beats):
        """
        Convert beats to time in seconds.

        Parameters
        ----------
        beats : float
            Time in beats

        Returns
        -------
        time : float
            Converted time in seconds.

        See also
        --------
        Project.time_to_beats
        """
        time = RPR.TimeMap2_QNToTime(self.id, beats)
        return time

    def begin_undo_block(self):
        """
        Start a new undo block.
        """
        RPR.Undo_BeginBlock2(self.id)

    @property
    def bpi(self):
        """
        Return project BPI (numerator of time signature).

        Returns
        -------
        bpi : float
            Numerator of time signature.
        """
        return self.time_signature[1]

    @reapy.inside_reaper()
    @property
    def bpm(self):
        """
        Project BPM (beats per minute).

        :type: float
        """
        return self.time_signature[0]

    @bpm.setter
    def bpm(self, bpm):
        """
        Set project BPM (beats per minute).

        Parameters
        ----------
        bpm : float
            Tempo in beats per minute.
        """
        RPR.SetCurrentBPM(self.id, bpm, True)

    @property
    def buffer_position(self):
        """
        Position of next audio block being processed in seconds.

        :type: float

        See also
        --------
        Project.play_position
            Latency-compensated actual-what-you-hear position.
        """
        return RPR.GetPlayPosition2Ex(self.id)

    @reapy.inside_reaper()
    def bypass_fx_on_all_tracks(self, bypass=True):
        """
        Bypass or un-bypass FX on all tracks.

        Parameters
        ----------
        bypass : bool
            Whether to bypass or un-bypass FX.
        """
        with self.make_current_project():
            RPR.BypassFxAllTracks(bypass)

    @property
    def can_redo(self):
        """
        Whether redo is possible.

        :type: bool
        """
        try:
            RPR.Undo_CanRedo2(self.id)
            can_redo = True
        except AttributeError:  # Bug in ReaScript API
            can_redo = False
        return can_redo

    @property
    def can_undo(self):
        """
        Whether undo is possible.

        :type: bool
        """
        try:
            RPR.Undo_CanUndo2(self.id)
            can_undo = True
        except AttributeError:  # Bug in ReaScript API
            can_undo = False
        return can_undo

    @property
    def cursor_position(self):
        """
        Edit cursor position in seconds.

        :type: float
        """
        position = RPR.GetCursorPositionEx(self.id)
        return position

    @cursor_position.setter
    def cursor_position(self, position):
        """
        Set edit cursor position.

        Parameters
        ----------
        position : float
            New edit cursor position in seconds.
        """
        RPR.SetEditCurPos(position, True, True)

    @reapy.inside_reaper()
    def disarm_rec_on_all_tracks(self):
        """
        Disarm record on all tracks.
        """
        with self.make_current_project():
            RPR.ClearAllRecArmed()

    def end_undo_block(self, description=""):
        """
        End undo block.

        Parameters
        ----------
        description : str
            Undo block description.
        """
        RPR.Undo_EndBlock2(self.id, description, 0)

    @reapy.inside_reaper()
    @property
    def focused_fx(self):
        """
        FX that has focus if any, else None.

        :type: FX or NoneType
        """
        if not self.is_current_project:
            return
        res = RPR.GetFocusedFX(0, 0, 0)
        if not res[0]:
            return
        if res[1] == 0:
            track = self.master_track
        else:
            track = self.tracks[res[1] - 1]
        if res[0] == 1:  # Track FX
            return track.fxs[res[3]]
        # Take FX
        item = track.items[res[2]]
        take = item.takes[res[3] // 2**16]
        return take.fxs[res[3] % 2**16]

    def get_play_rate(self, position):
        """
        Return project play rate at a given position.

        Parameters
        ----------
        position : float
            Position in seconds.

        Returns
        -------
        play_rate : float
            Play rate at the given position.

        See also
        --------
        Project.play_rate
            Project play rate at the current position.
        """
        play_rate = RPR.Master_GetPlayRateAtTime(position, self.id)
        return play_rate

    def get_selected_item(self, index):
        """
        Return index-th selected item.

        Parameters
        ----------
        index : int
            Item index.

        Returns
        -------
        item : Item
            index-th selected item.
        """
        item_id = RPR.GetSelectedMediaItem(self.id, index)
        item = reapy.Item(item_id)
        return item

    def get_selected_track(self, index):
        """
        Return index-th selected track.

        Parameters
        ----------
        index : int
            Track index.

        Returns
        -------
        track : Track
            index-th selected track.
        """
        track_id = RPR.GetSelectedTrack(self.id, index)
        track = reapy.Track(track_id)
        return track

    def glue_items(self, within_time_selection=False):
        """
        Glue items (action shortcut).

        Parameters
        ----------
        within_time_selection : bool
            If True, glue items within time selection.
        """
        action_id = 41588 if within_time_selection else 40362
        self.perform_action(action_id)

    @property
    def is_dirty(self):
        """
        Whether project is dirty (i.e. needing save).

        :type: bool
        """
        is_dirty = RPR.IsProjectDirty(self.id)
        return is_dirty

    @property
    def is_current_project(self):
        """
        Whether project is current project.

        :type: bool
        """
        is_current = self == Project()
        return is_current

    @reapy.inside_reaper()
    @property
    def items(self):
        """
        List of items in project.

        :type: list of Item
        """
        n_items = self.n_items
        item_ids = [RPR.GetMediaItem(self.id, i) for i in range(n_items)]
        return list(map(reapy.Item, item_ids))

    @property
    def length(self):
        """
        Project length in seconds.

        :type: float
        """
        length = RPR.GetProjectLength(self.id)
        return length

    @reapy.inside_reaper()
    @property
    def last_touched_fx(self):
        """
        Last touched FX and corresponding parameter index.

        :type: FX, int or NoneType, NoneType

        Notes
        -----
        Only Track FX are detected by this property. If last touched
        FX is a Take FX, this property is ``(None, None)``.

        Examples
        --------
        >>> fx, index = project.last_touched_fx
        >>> fx.name
        'VSTi: ReaSamplOmatic5000 (Cockos)'
        >>> fx.params[index].name
        "Volume"
        """
        if not self.is_current_project:
            fx, index = None, None
        else:
            res = RPR.GetLastTouchedFX(0, 0, 0)
            if not res[0]:
                fx, index = None, None
            else:
                if res[1]:
                    track = self.tracks[res[1] - 1]
                else:
                    track = self.master_track
                fx, index = track.fxs[res[2]], res[3]
        return fx, index

    def make_current_project(self):
        """
        Set project as current project.

        Can also be used as a context manager to temporarily set
        the project as current project and then go back to the original
        situation.

        Examples
        --------
        >>> p1 = reapy.Project()  # current project
        >>> p2 = reapy.Project(1)  # other project
        >>> p2.make_current_project()  # now p2 is current project
        >>> with p1.make_current_project():
        ...     do_something()  # current project is temporarily p1
        >>> # and p2 is current project again
        """
        return _MakeCurrentProject(self)

    def mark_dirty(self):
        """
        Mark project as dirty (i.e. needing save).
        """
        RPR.MarkProjectDirty(self.id)

    @reapy.inside_reaper()
    @property
    def markers(self):
        """
        List of project markers.

        :type: list of reapy.Marker
        """
        ids = [
            RPR.EnumProjectMarkers2(self.id, i, 0, 0, 0, 0, 0)
            for i in range(self.n_regions + self.n_markers)
        ]
        return [reapy.Marker(self, i[0]) for i in ids if not i[3]]

    @property
    def master_track(self):
        """
        Project master track.

        :type: Track
        """
        track_id = RPR.GetMasterTrack(self.id)
        master_track = reapy.Track(track_id)
        return master_track

    @reapy.inside_reaper()
    def mute_all_tracks(self, mute=True):
        """
        Mute or unmute all tracks.

        Parameters
        ----------
        mute : bool, optional
            Whether to mute or unmute all tracks (default=True).

        See also
        --------
        Project.unmute_all_tracks
        """
        with self.make_current_project():
            RPR.MuteAllTracks(mute)

    @property
    def n_items(self):
        """
        Number of items in project.

        :type: int
        """
        n_items = RPR.CountMediaItems(self.id)
        return n_items

    @property
    def n_markers(self):
        """
        Number of markers in project.

        :type: int
        """
        n_markers = RPR.CountProjectMarkers(self.id, 0, 0)[2]
        return n_markers

    @property
    def n_regions(self):
        """
        Number of regions in project.

        :type: int
        """
        n_regions = RPR.CountProjectMarkers(self.id, 0, 0)[3]
        return n_regions

    @property
    def n_selected_items(self):
        """
        Number of selected media items.

        :type: int
        """
        n_items = RPR.CountSelectedMediaItems(self.id)
        return n_items

    @property
    def n_selected_tracks(self):
        """
        Number of selected tracks in project (excluding master).

        :type: int
        """
        n_tracks = RPR.CountSelectedTracks2(self.id, False)
        return n_tracks

    @property
    def n_tempo_markers(self):
        """
        Number of tempo/time signature markers in project.

        :type: int
        """
        n_tempo_markers = RPR.CountTempoTimeSigMarkers(self.id)
        return n_tempo_markers

    @property
    def n_tracks(self):
        """
        Number of tracks in project.

        :type: int
        """
        n_tracks = RPR.CountTracks(self.id)
        return n_tracks

    @property
    def name(self):
        """
        Project name.

        :type: str
        """
        _, name, _ = RPR.GetProjectName(self.id, "", 2048)
        return name

    def pause(self):
        """
        Hit pause button.
        """
        RPR.OnPauseButtonEx(self.id)

    @property
    def path(self):
        """
        Project path.

        :type: str
        """
        _, path, _ = RPR.GetProjectPathEx(self.id, "", 2048)
        return path

    def perform_action(self, action_id):
        """
        Perform action with ID `action_id` in the main Actions section.

        Parameters
        ----------
        action_id : int
            Action ID in the main Actions section.
        """
        RPR.Main_OnCommandEx(action_id, 0, self.id)

    def play(self):
        """
        Hit play button.
        """
        RPR.OnPlayButtonEx(self.id)

    @property
    def play_position(self):
        """
        Latency-compensated actual-what-you-hear position in seconds.

        :type: float

        See also
        --------
        Project.buffer_position
            Position of next audio block being processed.
        """
        return RPR.GetPlayPositionEx(self.id)

    @property
    def play_rate(self):
        """
        Project play rate at the cursor position.

        :type: float

        See also
        --------
        Project.get_play_rate
            Return project play rate at a specified time.
        """
        play_rate = RPR.Master_GetPlayRate(self.id)
        return play_rate

    @property
    def play_state(self):
        """
        Project play state ("play", "pause" or "record").

        :type: str
        """
        states = {1: "play", 2: "pause", 4: "record"}
        state = states[RPR.GetPlayStateEx(self.id)]
        return state

    def redo(self):
        """
        Redo last action.

        Raises
        ------
        RedoError
            If impossible to redo.
        """
        success = RPR.Undo_DoRedo2(self.id)
        if not success:
            raise RedoError

    @reapy.inside_reaper()
    @property
    def regions(self):
        """
        List of project regions.

        :type: list of reapy.Region
        """
        ids = [
            RPR.EnumProjectMarkers2(self.id, i, 0, 0, 0, 0, 0)
            for i in range(self.n_regions + self.n_markers)
        ]
        return [reapy.Region(self, i[0]) for i in ids if i[3]]

    def save(self, force_save_as=False):
        """
        Save project.

        Parameters
        ----------
        force_save_as : bool
            Force using "Save as" instead of "Save".
        """
        RPR.Main_SaveProject(self.id, force_save_as)

    def select(self, start, end=None, length=None):
        if end is None:
            message = "Either `end` or `length` must be specified."
            assert length is not None, message
            end = start + length
        self.time_selection = start, end

    def select_all_items(self, selected=True):
        """
        Select or unselect all items, depending on `selected`.

        Parameters
        ----------
        selected : bool
            Whether to select or unselect items.
        """
        RPR.SelectAllMediaItems(self.id, selected)

    def select_all_tracks(self):
        """Select all tracks."""
        self.perform_action(40296)

    @property
    def selected_envelope(self):
        """
        Project selected envelope.

        :type: reapy.Envelope or None
        """
        envelope_id = RPR.GetSelectedTrackEnvelope(self.id)
        envelope = None if envelope_id == 0 else reapy.Envelope(envelope_id)
        return envelope

    @reapy.inside_reaper()
    @property
    def selected_items(self):
        """
        List of all selected items.

        :type: list of Item

        See also
        --------
        Project.get_selected_item
            Return a specific selected item.
        """
        return [
            reapy.Item(RPR.GetSelectedMediaItem(self.id, i))
            for i in range(self.n_items)
        ]

    @reapy.inside_reaper()
    @property
    def selected_tracks(self):
        """
        List of selected tracks (excluding master).

        :type: list of Track
        """
        return [
            reapy.Track(RPR.GetSelectedTrack(self.id, i))
            for i in range(self.n_selected_tracks)
        ]

    @selected_tracks.setter
    def selected_tracks(self, tracks):
        self.unselect_all_tracks()
        for track in tracks:
            track.select()

    @reapy.inside_reaper()
    def solo_all_tracks(self):
        """
        Solo all tracks in project.

        See also
        --------
        Project.unsolo_all_tracks
        """
        with self.make_current_project():
            RPR.SoloAllTracks(1)

    def stop(self):
        """
        Hit stop button.
        """
        RPR.OnStopButtonEx(self.id)

    @reapy.inside_reaper()
    @property
    def time_selection(self):
        """
        Project time selection.

        time_selection : reapy.TimeSelection

        Can be set and deleted as follows:

        >>> project = reapy.Project()
        >>> project.time_selection = 3, 8  # seconds
        >>> del project.time_selection
        """
        time_selection = reapy.TimeSelection(self)
        return time_selection

    @time_selection.setter
    def time_selection(self, selection):
        """
        Set time selection bounds.

        Parameters
        ----------
        selection : (float, float)
            Start and end of new time selection in seconds.
        """
        self.time_selection._set_start_end(*selection)

    @time_selection.deleter
    def time_selection(self):
        """
        Delete current time selection.
        """
        self.time_selection._set_start_end(0, 0)

    @property
    def time_signature(self):
        """
        Project time signature.

        This does not reflect tempo envelopes but is purely what is set in the
        project settings.

        bpm : float
            Project BPM (beats per minute)
        bpi : float
            Project BPI (numerator of time signature)
        """
        _, bpm, bpi = RPR.GetProjectTimeSignature2(self.id, 0, 0)
        return bpm, bpi

    def time_to_beats(self, time):
        """
        Convert time in seconds to beats.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        beats : float
            Time in beats.

        See also
        --------
        Projecr.beats_to_time
        """
        beats = RPR.TimeMap2_timeToQN(self.id, time)
        return beats

    @property
    def tracks(self):
        """
        List of project tracks.

        :type: TrackList
        """
        return reapy.TrackList(self)

    def undo(self):
        """
        Undo last action.

        Raises
        ------
        UndoError
            If impossible to undo.
        """
        success = RPR.Undo_DoUndo2(self.id)
        if not success:
            raise UndoError

    def unmute_all_tracks(self):
        """
        Unmute all tracks.
        """
        self.mute_all_tracks(mute=False)

    def unselect_all_tracks(self):
        """Unselect all tracks."""
        self.perform_action(40297)

    @reapy.inside_reaper()
    def unsolo_all_tracks(self):
        """
        Unsolo all tracks in project.

        See also
        --------
        Project.solo_all_tracks
        """
        with self.make_current_project():
            RPR.SoloAllTracks(0)


class _MakeCurrentProject:

    """Context manager used by Project.make_current_project."""

    def __init__(self, project):
        self.current_project = self._make_current_project(project)

    @staticmethod
    @reapy.inside_reaper()
    def _make_current_project(project):
        """Set current project and return the previous current project."""
        current_project = reapy.Project()
        RPR.SelectProjectInstance(project.id)
        return current_project

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current_project.make_current_project()
