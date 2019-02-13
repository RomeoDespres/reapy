from reapy import reascript_api as RPR
from reapy.tools import Program

class TimeSelection:    
    
    def __init__(self, parent_project):
        self.project_id = parent_project.id
        
    def _get_infos(self):
        """
        Return infos as returned by RPR.GetSet_LoopTimeRange2.
        
        Returns
        -------
        infos : tuple
            Time selection infos.
        """
        infos = RPR.GetSet_LoopTimeRange2(
            self.project_id, False, False, 0, 0, False
        )
        return infos
        
    @property
    def end(self):
        """
        Return time selection end in seconds.
        
        Returns
        -------
        end : float
            Time selection end in seconds.
        """
        infos = self._get_infos()
        end = infos[4]
        return end
        
    @end.setter
    def end(self, end):
        """
        Set time selection end.
        
        Parameters
        ----------
        end : float
            Time selection end in seconds.
        """
        code = """
        infos = RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        )
        infos[1], infos[4] = True, end
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id, end=end)
        
    @property
    def length(self)
        """
        Return time selection length in seconds.
        
        Returns
        -------
        length : float
            Time selection length in seconds.
        """
        infos = self._get_infos()
        start, end = infos[3:5]
        length = end - start
        return length
        
    @length.setter
    def length(self, length):
        """
        Set time selection length (by moving its end).
        
        Parameters
        ----------
        length : float
            Time selection length in seconds.
        """
        code = """
        infos = RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        )
        infos[1], infos[4] = True, infos[3] + length
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id, length=length)
        
    @property
    def start(self):
        """
        Return time selection start in seconds.
        
        Returns
        -------
        start : float
            Time selection start in seconds.
        """
        infos = self._get_infos()
        start = infos[3]
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
        code = """
        infos = RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        )
        infos[1], infos[3] = True, start
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id)
        
        

