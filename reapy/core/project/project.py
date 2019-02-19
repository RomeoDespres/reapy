"""Defines class Project."""

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program
from reapy.errors import RedoError, UndoError


class Project(ReapyObject):

    """REAPER project."""
    
    _class_name = "Project"

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
        return self.id == other.id
      
    @property
    def _args(self):
        return (self.id,)
        
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
        marker : Marker
            New marker.
            
        Notes
        -----
        If a marker with the same position and name already exists, no
        new marker will be created, and the existing marker index will
        be returned.
        """
        if isinstance(color, tuple):
            color = reapy.get_native_color(*color)
        marker_id = RPR.AddProjectMarker2(
            self.id, False, position, 0, name, -1, color
        )
        marker = Marker(self, marker_id)
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
        region : Region
            New region.
        """
        if isinstance(color, tuple):
            color = reapy.rgb_to_native(color)
        region_id = RPR.AddProjectMarker2(
            self.id, True, start, end, name, -1, color
        )
        region = Region(self, region_id)
        return region
        
    def add_track(self, index=0):
        """
        Add track at a specified index.
        
        Parameters
        ----------
        index : int
            Index at which to insert track.
            
        Returns
        -------
        track : Track
            New track.
        """
        code = """
        current_project = reapy.Project()
        project.make_current_project()
        RPR.InsertTrackAtIndex(index, True)
        current_project.make_current_project()
        track_id = RPR.GetTrack(project.id, index)
        """
        track_id = Program(code, "track_id").run(
            project=self, index=index
        )[0]
        track = Track(track_id)
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

    @property
    def bpm(self):
        """
        Return project BPM (beats per minute).

        Returns
        -------
        bpm : float
            Project BPM (beats per minute).
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
        
    def bypass_fx_on_all_tracks(self, bypass=True):
        """
        Bypass or un-bypass FX on all tracks.
        
        Parameters
        ----------
        bypass : bool
            Whether to bypass or un-bypass FX.
        """
        code = """
        current_project = reapy.Project()
        project.make_current_project()
        RPR.BypassFxAllTracks(bypass)
        current_project.make_current_project()
        """
        Program(code).run(project=self, bypass=bypass)
        
    @property
    def can_redo(self):
        """
        Return whether redo is possible.
        
        Returns
        -------
        can_redo : bool
            Whether redo is possible.
        """
        try:
            RPR.Undo_CanRedo2(self.id)
            can_redo = True
        except AttributeError: # Bug in ReaScript API when 
            can_redo = False
        return can_redo
    
    @property
    def can_undo(self):
        """
        Return whether undo is possible.
        
        Returns
        -------
        can_undo : bool
            Whether undo is possible.
        """
        try:
            RPR.Undo_CanUndo2(self.id)
            can_undo = True
        except AttributeError: # Bug in ReaScript API when 
            can_undo = False
        return can_undo
    
    @property
    def cursor_position(self):
        """
        Return edit cursor position in seconds.
        
        Returns
        -------
        position : float
            Edit cursor position in seconds.
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
        
    def disarm_rec_on_all_tracks(self):
        """
        Disarm record on all tracks.
        """
        code = """
        current_project = reapy.Project()
        project.make_current_project()
        RPR.ClearAllRecArmed()
        current_project.make_current_project()
        """
        Program(code).run(project=self)
        
    def end_undo_block(self, description=""):
        """
        End undo block.
        
        Parameters
        ----------
        description : str
            Undo block description.
        """
        RPR.Undo_EndBlock2(self.id, description, 0)
        
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
        item = Item(item_id)
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
        track = Track(track_id)
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
        Return whether project is dirty (i.e. needing save).
        
        Returns
        -------
        is_dirty : bool
            Whether project is dirty.
        """
        is_dirty = RPR.IsProjectDirty(self.id)
        return is_dirty
        
    @property
    def is_current_project(self):
        """
        Return whether project is current project.
        
        Returns
        -------
        is_current : bool
            Whether project is current project.
        """
        is_current = self == Project()
        return is_current

    @property
    def length(self):
        """
        Return project length in seconds.

        Returns
        -------
        length : float
            Project length in seconds.
        """
        length = RPR.GetProjectLength(self.id)
        return length
        
    def make_current_project(self):
        """
        Set project as current project.
        """
        RPR.SelectProjectInstance(self.id)
        
    def mark_dirty(self):
        """
        Mark project as dirty (i.e. needing save).
        """
        RPR.MarkProjectDirty(self.id)
    
    @property
    def markers(self):
        """
        Return list of project markers.
        
        Returns
        -------
        markers : list of Marker
            List of project markers.
        """
        code = """
        n_markers = project.n_markers
        ids = [
            RPR.EnumProjectMarkers2(project.id, i, 0, 0, 0, 0, 0)
            for i in range(project.n_regions + project.n_markers)
        ]
        ids = [
            i[0] for i in ids if not i[3]
        ]
        """
        ids = Program(code, "ids").run(project=self)[0]
        markers = [Marker(self, i) for i in ids]
        return markers
        
    @property
    def master_track(self):
        """
        Return project master track.
        
        Returns
        -------
        master_track : Track
            Project master track.
        """
        track_id = RPR.GetMasterTrack(self.id)
        master_track = Track(track_id)
        return master_track
        
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
        code = """
        current_project = reapy.Project()
        project.make_current_project()
        RPR.MuteAllTracks(mute)
        current_project.make_current_project()
        """
        Program(code).run(project=self, mute=mute)
        
    @property
    def n_items(self):
        """
        Return number of items in project.
        
        Returns
        -------
        n_items : int
            Number of items in project.
        """
        n_items = RPR.CountMediaItems(self.id)
        return n_items
        
    @property
    def n_markers(self):
        """
        Return number of markers a in project.
        
        Returns
        -------
        n_markers : int
            Number of markers in project.
        """
        n_markers = RPR.CountProjectMarkers(self.id, 0, 0)[2]
        return n_markers
        
    @property
    def n_regions(self):
        """
        Return number of regions in project.
        
        Returns
        -------
        n_regions : int
            Number of regions in project.
        """
        n_regions = RPR.CountProjectMarkers(self.id, 0, 0)[3]
        return n_regions
        
    @property
    def n_selected_items(self):
        """
        Return the number of selected media items.

        Returns
        -------
        n_items : int
            Number of selected media items.
        """
        n_items = RPR.CountSelectedMediaItems(self.id)
        return n_items
        
    @property
    def n_selected_tracks(self):
        """
        Return number of selected tracks in project (excluding master).
        
        Returns
        -------
        n_tracks : int
            Number of selected tracks in project.
        """
        n_tracks = RPR.CountSelectedTracks2(self.id, False)
        return n_tracks
        
    @property
    def n_tempo_markers(self):
        """
        Return number of tempo/time signature markers in project.
        
        Returns
        -------
        n_tempo_markers : int
            Number of tempo/time signature markers in project.
        """
        n_tempo_markers = RPR.CountTempoTimeSigMarkers(self.id)
        return n_tempo_markers
        
    @property
    def n_tracks(self):
        """
        Return the number of tracks in project.
        
        Returns
        -------
        n_tracks : int
            Number of tracks in project.
        """
        n_tracks = RPR.CountTracks(self.id)
        return n_tracks
         
    @property
    def name(self):
        """
        Return project name.
        
        Returns
        -------
        name : str
            Project name.
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
        Return project path.
        
        Returns
        -------
        path : str
            Project path.
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
    def play_rate(self):
        """
        Return project play rate.
        
        Returns
        -------
        play_rate : float
            Project play rate.
        """
        play_rate = RPR.Master_GetPlayRate(self.id)
        return play_rate

    @property
    def play_state(self):
        """
        Return project play state.
        
        Returns
        -------
        state : {"play", "pause", "record"}
            Project play state.
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
            
    @property
    def regions(self):
        """
        Return list of project regions.
        
        Returns
        -------
        regions : list of Region
            List of project regions.
        """
        code = """
        ids = [
            RPR.EnumProjectMarkers2(project.id, i, 0, 0, 0, 0, 0)
            for i in range(project.n_regions + project.n_markers)
        ]
        ids = [
            i[0] for i in ids if i[3]
        ]
        """
        ids = Program(code, "ids").run(project=self)[0]
        regions = [Region(self, i) for i in ids]
        return regions
        
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
        
    @property
    def selected_envelope(self):
        """
        Return project selected envelope.
        
        Returns
        -------
        envelope : Envelope or None
            Selected envelope if any, else None.
        """
        envelope_id = RPR.GetSelectedTrackEnvelope(self.id)
        envelope = None if envelope_id == 0 else Envelope(envelope_id)
        return envelope

    @property
    def selected_items(self):
        """
        Return list of all selected items.

        Returns
        -------
        items : list of Item
            List of all selected items.

        See also
        --------
        Project.get_selected_item
            Return a specific selected item.
        """
        code = """
        n_items = RPR.CountSelectedMediaItems(project_id)
        item_ids = [
            RPR.GetSelectedMediaItem(project_id, i) for i in range(n_items)
        ]
        """
        item_ids = Program(code, "item_ids").run(project_id=self.id)[0]
        items = list(map(Item, item_ids))
        return items
    
    @property
    def selected_tracks(self):
        """
        Return list of selected tracks (excluding master).
        
        Returns
        -------
        tracks : list of Track
            List of selected tracks.
        """
        code = """
        track_ids = [
            RPR.GetSelectedTrack(project_id, i)
            for i in range(reapy.Project(project_id).n_selected_tracks)
        ]
        """
        track_ids = Program(code, "track_ids").run(project_id=self.id)[0]
        tracks = list(map(Track, track_ids))
        return tracks
        
        
    def stop(self):
        """
        Hit stop button.
        """
        RPR.OnStopButtonEx(self.id)
        
    @property
    def time_selection(self):
        """
        Return project time selection.
        
        Returns
        -------
        time_selection : TimeSelection
            Project time selection.
        """
        time_selection = TimeSelection(self)
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
        code = """
        project.time_selection.start = selection[0]
        project.time_selection.end = selection[1]
        """
        Program(code).run(project=self, selection=selection)

    @property
    def time_signature(self):
        """
        Return project time signature.

        This does not reflect tempo envelopes but is purely what is set in the
        project settings.

        Returns
        -------
        bpm : float
            Project BPM (beats per minute)
        bpi : float
            Project BPI (numerator of time signature)
        """
        _, bpm, bpi = RPR.GetProjectTimeSignature2(self.id, 0, 0)
        return bpm, bpi
    
    @property    
    def tracks(self):
        """
        Return list of project tracks.
        
        Returns
        -------
        tracks : list of Track
            List of project tracks.
        """
        code = """
        n_tracks = RPR.CountTracks(project_id)
        track_ids = [RPR.GetTrack(project_id, i) for i in range(n_tracks)]
        """
        track_ids = Program(code, "track_ids").run(project_id=self.id)[0]
        tracks = [Track(track_id) for track_id in track_ids]
        return tracks
        
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
 

from ..item.item import Item
from ..track.envelope import Envelope
from ..track.track import Track
from .marker import Marker
from .region import Region
from .time_selection import TimeSelection
