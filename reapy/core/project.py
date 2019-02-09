import reapy

if not reapy.is_inside_reaper():
    from reapy.reascript_api.dist_api.api_function import APISequence
from reapy import reascript_api as RPR


class Project:

    def __init__(self, id=0):
        self.id = id
        
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

    @property
    def cursor_position(self):
        position = RPR.GetCursorPositionEx(self.id)
        return position

    @cursor_position.setter
    def cursor_position(self, position):
        RPR.SetEditCurPos(position, True, True)

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
        ReaProject.get_selected_item
            Return a specific selected item.
        """
        n_items = self.count_selected_items()
        functions = [RPR.GetSelectedMediaItem]*n_items
        args = [(self.id, i) for i in range(n_items)]
        ids = APISequence(*functions)(*args)
        items = [Item(item_id) for item_id in ids]
        return items

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
        n_tracks = self.count_tracks()
        functions = [RPR.GetTrack]*n_tracks
        args = [(self.id, i) for i in range(n_tracks)]
        ids = APISequence(*functions)(*args)
        tracks = [Track(track_id) for track_id in ids]
        return tracks
        
    def add_midi_item(self, start=None, end=None, length=None, quantize=False):
        message = "`end` and `length` can't be both specified"
        assert end is None or length is None, message
        # TODO
        
    def add_marker(self, position, name="", color=0):
        """
        Create new marker and return its index.
        
        Parameters
        ----------
        position : float
            Marker position in seconds.
        name : str, optional
            Marker name.
        color : int, tuple, optional
            Marker color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.
            
        Returns
        -------
        marker_id : int
            The marker index.
            
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
        return marker_id
    
    def add_region(self, start, end, name=""):
        """
        Create new marker and return its index.
        
        Parameters
        ----------
        start : float
            Region start in seconds.
        end : float
            Region end in seconds.
        name : str, optional
            Region name.
        color : int, tuple, optional
            Marker color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.
            
        Returns
        -------
        region_id : int
            The region index.
        """
        if isinstance(color, tuple):
            color = reapy.rgb_to_native(color)
        region_id = RPR.AddProjectMarker(
            self.id, True, start, end, name, -1, color
        )
        return region_id

    def count_selected_items(self):
        """
        Return the number of selected media items.

        Returns
        -------
        n_items : int
            Number of selected media items.
        """
        n_items = RPR.CountSelectedMediaItems(self.id)
        return n_items
        
    def count_tracks(self):
        """
        Return the number of tracks in project.
        
        Returns
        -------
        n_tracks : int
            Number of tracks in project.
        """
        n_tracks = RPR.CountTracks(self.id)
        return n_tracks

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

    def perform_action(self, action_id):
        """
        Perform action with ID `action_id` in the main Actions section.

        Parameters
        ----------
        action_id : int
            Action ID in the main Actions section.
        """
        RPR.Main_OnCommandEx(action_id, 0, self.id)
        
    def select_all_items(self, selected=True):
        """
        Select or unselect all items, depending on `selected`.

        Parameters
        ----------
        selected : bool
            Whether to select or unselect items.
        """
        RPR.SelectAllMediaItems(self.id, selected)

    def _get_selected_item(self, index):
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

from .item import Item
