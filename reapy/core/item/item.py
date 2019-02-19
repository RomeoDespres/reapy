import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program


class Item(ReapyObject):

    _class_name = "Item"

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Item)
    
    @property
    def _args(self):
        return (self.id,)

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
        
    def get_info_value(self, param_name):
        value = RPR.GetMediaItemInfo_Value(self.id, param_name)
        return value
        
    def get_take(self, index):
        """
        Return index-th take of item.

        Parameters
        ----------
        index : int
            Take index.

        Returns
        -------
        take : Take
            index-th take of media item.
        """
        take_id = RPR.GetItemTake(self.id, i)
        take = Take(take_id)
        return take
        
    @property
    def is_selected(self):
        """
        Return whether item is selected.
        
        Returns
        -------
        is_selected : bool
            Whether item is selected.
        """
        is_selected = bool(RPR.IsMediaItemSelected(self.id))
        return is_selected

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
        length = self.get_info_value(param_name)
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
    def n_takes(self):
        """
        Return the number of takes of media item.

        Returns
        -------
        n_takes : int
            Number of takes of media item.
        """
        n_takes = RPR.GetMediaItemNumTakes(self.id)
        return n_takes

    @property
    def position(self):
        """
        Return item position in seconds.

        Returns
        -------
        position : float
            Item position in seconds.
        """
        position = self.get_info_value("D_POSITION")
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
        
    def split(self, position):
        """
        Split item and return left and right parts.
        
        Parameters
        ----------
        position : float
            Split position in seconds.
        
        Returns
        -------
        left, right : Item
            Left and right parts of the split.
        """
        right_id = RPR.SplitMediaItem(self.id, position)
        left, right = self, Item(right_id)
        return left, right

    @property
    def takes(self):
        """
        Return list of all takes of media item.

        Returns
        -------
        takes : list
            List of all takes of media item.
        """
        code = """
        n_takes = RPR.GetMediaItemNumTakes(item_id)
        take_ids = [RPR.GetMediaItemTake(item_id, i) for i in range(n_takes)]
        """
        take_ids = Program(code, "take_ids").run(item_id=self.id)[0]
        takes = [Take(take_id) for take_id in take_ids]
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

class MIDIItem(Item):

    pass


from ..project.project import Project
from ..track.track import Track
from .take import Take

