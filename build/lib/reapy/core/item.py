from reapy import reascript_api as RPR


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
    def position(self, value):
        RPR.SetitemPosition(self.id, value, False)

    @property
    def takes(self):
        """
        Return list of all takes of media item.

        Returns
        -------
        takes : list
            List of all takes of media item.
        """
        takes = [
            self._get_take(i) for i in range(self.count_takes())
        ]
        return takes
        
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

from .take import Take
