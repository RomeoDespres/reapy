import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Item(ReapyObject):

    _class_name = "Item"

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

    @property
    def _args(self):
        return self.id,

    @property
    def active_take(self):
        """
        Return the active take of the item.

        Returns
        -------
        take : Take
            Active take of the item.
        """
        take = reapy.Take(RPR.GetActiveTake(self.id))
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
        take = reapy.Take(take_id)
        return take

    @reapy.inside_reaper()
    def delete(self):
        """Delete item."""
        RPR.DeleteTrackMediaItem(self.track.id, self.id)

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
        take_id = RPR.GetItemTake(self.id, index)
        take = reapy.Take(take_id)
        return take

    @reapy.inside_reaper()
    @property
    def has_valid_id(self):
        """
        Whether ReaScript ID is still valid.

        For instance, if item has been deleted, ID will not be valid
        anymore.

        :type: bool
        """
        try:
            project_id = self.project.id
        except OSError:
            return False
        pointer, name = self._get_pointer_and_name()
        return bool(RPR.ValidatePtr2(project_id, pointer, name))

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
        Item parent project.

        :type: reapy.Project
        """
        return reapy.Project(RPR.GetItemProjectContext(self.id))

    def set_info_value(self, param_name, value):
        return RPR.SetMediaItemInfo_Value(self.id, param_name, value)

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

    @reapy.inside_reaper()
    @property
    def takes(self):
        """
        Return list of all takes of media item.

        Returns
        -------
        takes : list of Take
            List of all takes of media item.
        """
        n_takes = RPR.GetMediaItemNumTakes(self.id)
        take_ids = [RPR.GetMediaItemTake(self.id, i) for i in range(n_takes)]
        takes = [reapy.Take(take_id) for take_id in take_ids]
        return takes

    @reapy.inside_reaper()
    @property
    def track(self):
        """
        Parent track of item.

        Set it by passing a track, or a track index.

        :type: Track

        Examples
        --------
        >>> track0, track1 = project.tracks[0:2]
        >>> item = track0.items[0]
        >>> item.track == track0
        True
        >>> item.track = track1  # Move to track 1
        >>> item.track = 0  # Move to track 0
        """
        track_id = RPR.GetMediaItemTrack(self.id)
        track = reapy.Track(track_id)
        return track

    @track.setter
    def track(self, track):
        if isinstance(track, int):
            track = reapy.Track(track, project=self.project)
        RPR.MoveMediaItemToTrack(self.id, track.id)

    def update(self):
        """Update item in REAPER interface."""
        RPR.UpdateItemInProject(self.id)
