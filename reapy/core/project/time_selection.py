from reapy import reascript_api as RPR

class TimeSelection:    
    
    def __init__(self, parent_project):
        self.project_id = parent_project.id
        
    @property
    def start(self):
        """
        Return time selection start in seconds.
        
        Returns
        -------
        start : float
            Time selection start in seconds.
        """
        _, _, _, start, _, _ = RPR.GetSet_LoopTimeRange2(
            self.project_id, False, False, 0, 0, False
        )
        return start
        
    @start.setter
    def start(self, start):
        """
        Set time selection start.
        
        Parameters
        ----------
        start : float
            New time selection start.
        """
        infos = RPR.GetSet_LoopTimeRange2(
            self.project_id, False, False, 0, 0, False
        )
        infos[1], infos[3] = True, start
        RPR.GetSet_LoopTimeRange2(*infos) 
        

