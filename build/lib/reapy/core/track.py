from reapy import reascript_api


class Track:

    def __init__(self, id):
        self.id = id
        
    def add_item(self):
        """
        Create new item on track and return it.
        
        Returns
        -------
        item : Item
            New item on track.
        """
        item_id = reascript_api.RPR_AddMediaItemToTrack(self.id)
        item = Item(item_id)
        return item
        
        
from .item import Item