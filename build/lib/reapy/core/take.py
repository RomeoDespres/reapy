from reapy import reascript_api as RPR


class Take:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Take)

    @property
    def data(self):
        data = self.source.data
        start_offset = self.start_offset
        length = self.item.length
        sample_rate = self.source.sample_rate
        data = data[int(sample_rate*start_offset):int(sample_rate*length)]
        return data

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
        start_offset = self._get_info_value("D_STARTOFFS")
        return start_offset

    def _get_info_value(self, param_name):
        value = RPR.GettakeInfo_Value(self.id, param_name)
        return value

from .item import Item
from .source import Source
