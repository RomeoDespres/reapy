from reapy import reascript_api as RPR


class Take:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Take)
        
    def get_info_value(self, param_name):
        value = RPR.GettakeInfo_Value(self.id, param_name)
        return value

    @property
    def item(self):
        """
        Return parent item.

        Returns
        -------
        item : item
            Parent item.
        """
        item = Item(RPR.Gettake_Item(self.id))
        return item

    @property
    def source(self):
        """
        Return take source.

        Returns
        -------
        source : Source
            Take source.
        """
        source = Source(RPR.GetMediaItemTake_Source(self.id))
        return source

    @property
    def start_offset(self):
        """
        Return start time of the take relative to start of source file.

        Returns
        -------
        start_offset : float
            Start offset in seconds.
        """
        start_offset = self.get_info_value("D_STARTOFFS")
        return start_offset
        
    @property
    def track(self):
        """
        Return parent track of take.
        
        Returns
        -------
        track : Track
            Parent track of take.
        """
        track_id = RPR.GetMediaItemTake_Track(self.id)
        track = Track(track_id)
        return track

    
from ..track.track import Track
from .item import Item
from .source import Source
