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
        infos = list(RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        ))
        infos[1], infos[4] = True, end
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id, end=end)
        
    @property
    def length(self):
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
        infos = list(RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        ))
        infos[1], infos[4] = True, infos[3] + length
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id, length=length)
        
    @property
    def looping(self):
        """
        Return whether looping is enabled.
        
        Returns
        -------
        looping : bool
            Whether looping is enabled.
        """
        looping = bool(RPR.GetSetRepeatEx(self.project_id, -1))
        return looping
        
    @looping.setter
    def looping(self, looping):
        """
        Sets whether time selection should loop.
        
        Parameters
        ----------
        looping : bool
            Whether time selection should loop.
        """
        looping = 1 if looping else 0
        RPR.GetSetRepeatEx(self.project_id, looping)
        
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
        infos = list(RPR.GetSet_LoopTimeRange2(
            project_id, False, False, 0, 0, False
        ))
        infos[1], infos[3] = True, start
        RPR.GetSet_LoopTimeRange2(*infos)
        """
        Program(code).run(project_id=self.project_id, start=start)
        
    def shift(self, direction=""):
        """
        Shift time selection.
        
        Parameters
        ----------
        direction : {"right", "left"}
            Direction to which time selection will be shifted. Nothing
            happens if direction is neither "right" nor "left". Note
            that the shift size depends on whether snap is enabled
            and of the zoom level.
        """
        if direction == "right":
            RPR.Loop_OnArrow(self.project_id, 1)
        elif direction == "left":
            RPR.Loop_OnArrow(self.project_id, -1)
        
        

