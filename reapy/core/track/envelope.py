from reapy import reascript_api as RPR


UNDEFINED_ENVELOPE_ID = "(TrackEnvelope*)0x0000000000000000"


class Envelope:
    
    def __init__(self, id):
        self.id = id
        
    @property
    def n_items(self):
        """
        Return number of automation items in envelope.
        
        Returns
        -------
        n_items : int
            Number of automation items in envelope.
        """
        n_items = RPR.CountAutomationPoints(self.id)
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