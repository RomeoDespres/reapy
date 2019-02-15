from reapy import reascript_api as RPR


UNDEFINED_ENVELOPE_ID = "(TrackEnvelope*)0x0000000000000000"


class Envelope:
    
    def __init__(self, id):
        self.id = id
        
    def add_item(self, position=0., length=0., pool=0):
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
        item : AutomationItem
            New automation item.
        """
        item_index = RPR.InsertAutomationItem(self.id, pool, position, length)
        item = AutomationItem(envelope=self, index=item_index)
        return item
        
    @property
    def n_items(self):
        """
        Return number of automation items in envelope.
        
        Returns
        -------
        n_items : int
            Number of automation items in envelope.
        """
        n_items = RPR.CountAutomationItems(self.id)
        return n_items
        
    @property
    def n_points(self):
        """
        Return number of points in envelope.
        
        Returns
        -------
        n_points : int
            Number of points in envelope.
        """
        n_points = RPR.CountEnvelopePoints(self.id)
        return n_points
        

class UndefinedEnvelopeError(Exception):
    
    def __init__(self, index, name, chunk_name):
        if index is not None:
            message = "No envelope with index {}".format(index)
        elif name is not None:
            message = "No envelope with name {}".format(name)
        else:
            message = "No envelope with chunk name {}".format(chunk_name)
        super(UndefinedEnvelopeError, self).__init__(message)
        

from .automation_item import AutomationItem