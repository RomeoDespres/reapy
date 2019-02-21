from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Envelope(ReapyObject):

    _class_name = "Envelope"

    def __init__(self, id):
        self.id = id

    @property
    def _args(self):
        return (self.id,)

    def add_item(self, position=0., length=1., pool=0):
        """
        Add automation item to envelope.

        Parameters
        ----------
        position : float, optional
            New item position in seconds (default=0).
        length : float
            New item length in seconds (default=0).
        pool : int
            New item pool index. If >= 0 the automation item will be a
            new instance of that pool (which will be created as an
            empty instance if it does not exist).

        Returns
        -------
        item : reapy.AutomationItem
            New automation item.
        """
        item_index = RPR.InsertAutomationItem(self.id, pool, position, length)
        item = reapy.AutomationItem(envelope=self, index=item_index)
        return item

    def delete_points_in_range(self, start, end):
        """
        Delete envelope points between `start` and `end`.

        Parameters
        ----------
        start : float
            Range start in seconds.
        end : float
            Range end in seconds.
        """
        RPR.DeleteEnvelopePointRange(self.id, start, end)

    @property
    def items(self):
        """
        List of automation items in envelope.

        :type: list of reapy.AutomationItem
        """
        n_items = self.n_items
        items = [reapy.AutomationItem(self, i) for i in range(n_items)]
        return items

    @property
    def n_items(self):
        """
        Number of automation items in envelope.

        :type: int
        """
        n_items = RPR.CountAutomationItems(self.id)
        return n_items

    @property
    def n_points(self):
        """
        Number of points in envelope.

        :type: int
        """
        n_points = RPR.CountEnvelopePoints(self.id)
        return n_points

    @property
    def name(self):
        """
        Envelope name.
        
        :type: str
        """
        name = RPR.GetEnvelopeName(self.id, "", 2048)[2]
        return name
