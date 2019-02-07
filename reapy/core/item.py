import reapy
from reapy import reascript_api as RPR
if not reapy.is_inside_reaper():
    from reapy.reascript_api.dist_api.api_function import APISequence


class Item:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Item)

    @property
    def active_take(self):
        """
        Return the active take of the item.

        Returns
        -------
        take : Take
            Active take of the item.
        """
        take = Take(RPR.GetActiveTake(self.id))
        return take

    @property
    def length(self):
        """
        Return item length in seconds.

        Returns
        -------
        length : float
            Item length in seconds.
        """
        param_name = "D_LENGTH"
        length = self._get_info_value(param_name)
        return length
        
    @length.setter
    def length(self, length):
        """
        Set item length.
        
        Parameters
        ----------
        length : float
            New item length in seconds.
        """
        RPR.SetMediaItemLength(self.id, length, True)

    @property
    def position(self):
        """
        Return item position in seconds.

        Returns
        -------
        position : float
            Item position in seconds.
        """
        position = RPR.GetitemInfo_Value(self.id, "D_POSITION")
        return position

    @position.setter
    def position(self, position):
        """
        Set media item position to `position`.
        
        Parameters
        ----------
        position : float
            New item position in seconds.
        """
        RPR.SetMediaItemPosition(self.id, position, False)
        
    @property
    def project(self):
        """
        Return item parent project.
        
        Returns
        -------
        project : Project
            Item parent project.
        """
        project_id = RPR.GetItemProjectContext(self.id)
        project = Project(project_id)
        return project

    @property
    def takes(self):
        """
        Return list of all takes of media item.

        Returns
        -------
        takes : list
            List of all takes of media item.
        """
        n_takes = self.count_takes()
        if not reapy.is_inside_reaper():
            functions = [RPR.GetItemTake]*n_takes
            args = [(self.id, i) for i in range(n_takes)]
            ids = APISequence(*functions)(*args)
            takes = [Take(take_id) for take_id in ids]
        else:
            takes = [
                self._get_take(i) for i in range(n_takes)
            ]
        return takes
        
    @property
    def track(self):
        """
        Return parent track of item.
        
        Returns
        -------
        track : Track
            Parent track of item.
        """
        track_id = RPR.GetMediaItemTrack(self.id)
        track = Track(track_id)
        return track
        
    @track.setter
    def track(self, track):
        """
        Move item to track `track`.
        
        Parameters
        ----------
        track : Track, int
            If Track, destination track for item. If int, track index.
            
        Raises
        ------
        Exception
            If operation failed within REAPER.
        """
        if isisintance(track, int):
            track = Track(track, project=self.project)
        success = RPR.MoveMediaItemToTrack(self.id, track.id)
        if not success:
            raise Exception("Couldn't move item to track.")
        
    def add_take(self):
        """
        Create and return a new take in item.
        
        Returns
        -------
        take : Take
            New take in item.
        """
        take_id = RPR.AddTakeToMediaItem(self.id)
        take = Take(take_id)
        return take

    def count_takes(self, id):
        """
        Return the number of takes of media item.

        Returns
        -------
        n_takes : int
            Number of takes of media item.
        """
        n_takes = RPR.GetitemNumTakes(self.id)
        return n_takes

    def _get_info_value(self, param_name):
        value = RPR.GetitemInfo_Value(self.id, param_name)
        return value
    
    def _get_take(self, i):
        """
        Return i-th take of item.

        Parameters
        ----------
        i : int
            Take index.

        Returns
        -------
        take : Take
            i-th take of media item.
        """
        take_id = RPR.GetitemTake(self.id, i)
        take = Take(take_id)
        return take

from .project import Project
from .take import Take
from .track import Track
