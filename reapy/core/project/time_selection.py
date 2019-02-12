from reapy import reascript_api as RPR

class TimeSelection:    
    
    def __init__(self, parent_project):
        self.project_id = parent_project.id
        
    @property
    def start(self):
        _, _, _, start, _, _ = RPR.GetSet_LoopTimeRange2(
            self.project_id, False, None, None, None, None
        )
        return start
        

