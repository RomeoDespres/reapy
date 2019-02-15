from reapy import reascript_api as RPR

class AutomationItem:

    def __init__(self, envelope, index):
        self.envelope_id = envelope.id
        self.index = index
        
    @property
    def length(self):
        """
        Return item length in seconds.
        
        Returns
        -------
        length : float
            Item length in seconds.
        """
        length = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_LENGTH", 0, False
        )
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
        success = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_LENGTH", length, True
        )
        
    @property
    def pool(self):
        """
        Return item pool.
        
        Returns
        -------
        pool : int
            Item pool.
        """
        pool = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_POOL", 0, False
        )
        return pool
        
    @pool.setter
    def pool(self, pool):
        """
        Set item pool.
        
        Parameters
        ----------
        pool : int
            New item pool.
        """
        success = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_POOL", pool, True
        )
        
    @property
    def position(self):
        """
        Return item position in seconds.
        
        Returns
        -------
        position : float
            Item position in seconds.
        """
        position = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_POSITION", 0, False
        )
        return position
        
    @position.setter
    def position(self, position):
        """
        Set item position.
        
        Parameters
        ----------
        position : float
            New item position in seconds.
        """
        success = RPR.GetSetAutomationItemInfo(
            self.envelope_id, self.index, "D_POSITION", position, True
        )