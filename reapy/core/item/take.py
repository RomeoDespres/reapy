from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program


class Take(ReapyObject):
    
    _class_name = "Take"

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id
     
    @property
    def _args(self):
        return (self.id,)
        
    def get_info_value(self, param_name):
        value = RPR.GettakeInfo_Value(self.id, param_name)
        return value
        
    @property
    def is_active(self):
        """
        Return whether take is active.
        
        Returns
        -------
        is_active : bool
            Whether take is active.
        """
        code = """
        from reapy.core.item.take import Take
        take = Take(take_id)
        is_active = take == take.item.active_take
        """
        is_active = Program(code, "is_active").run(take_id=self.id)[0]
        return is_active

    @property
    def item(self):
        """
        Return parent item.

        Returns
        -------
        item : item
            Parent item.
        """
        item = Item(RPR.GetMediaItemTake_Item(self.id))
        return item
        
    def make_active_take(self):
        """
        Make take active.
        """
        RPR.SetActiveTake(self.id)
        
    @property
    def n_envelopes(self):
        """
        Return number of envelopes on take.
        
        Returns
        -------
        n_envelopes : int
            Number of envelopes on take.
        """
        n_envelopes = RPR.CountTakeEnvelopes(self.id)
        return n_envelopes

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
