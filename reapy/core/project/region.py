import reapy
from reapy import reascript_api as RPR
from reapy.tools import Program

class Region:

    def __init__(
        self, parent_project=None, index=None, parent_project_id=None
    ):
        if parent_project_id is None:
            message = (
                "One of `parent_project` or `parent_project_id` must be "
                "specified."
            )
            assert parent_project is not None, message
            parent_project_id = parent_project.id
        self.project_id = parent_project_id
        self.index = index
        
    def _to_dict(self):
        return {
            "__reapy__": True,
            "class": "Region",
            "args": (),
            "kwargs": {
                "index": self.index, "parent_project_id": self.project_id
            }
        }
        
    def _get_enum_index(self):
        """
        Return region index as needed by RPR.EnumProjectMarkers2.
        """
        code = """
        index = [
            i for i, r in enumerate(project.regions)
            if r.index == region.index
        ][0]
        """
        index = Program(code, "index").run(
            region=self, project=reapy.Project(self.project_id)
        )[0]
        return index
        
    @property
    def end(self):
        """
        Return region end.
        
        Returns
        -------
        end : float
            Region end in seconds.
        """
        code = """
        index = region._get_enum_index()
        end = RPR.EnumProjectMarkers2(
            region.project_id, index, 0, 0, 0, 0, 0
        )[5]
        """
        end = Program(code, "end").run(region=self)[0]
        return end
        
    @end.setter
    def end(self, end):
        """
        Set region end.
        
        Parameters
        ----------
        end : float
            region end in seconds.
        """
        code = """
        RPR.SetProjectMarker2(
            region.project_id, region.index, True, region.start, end, ""
        )
        """
        Program(code).run(region=self, end=end)
        
    def delete(self):
        """
        Delete region.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, True)
        
    @property
    def start(self):
        """
        Return region start.
        
        Returns
        -------
        start : float
            Region start in seconds.
        """
        code = """
        index = region._get_enum_index()
        start = RPR.EnumProjectMarkers2(
            region.project_id, index, 0, 0, 0, 0, 0
        )[4]
        """
        start = Program(code, "start").run(region=self)[0]
        return start
        
    @start.setter
    def start(self, start):
        """
        Set region start.
        
        Parameters
        ----------
        start : float
            region start in seconds.
        """
        code = """
        RPR.SetProjectMarker2(
            region.project_id, region.index, 1, start, region.end, ""
        )
        """
        Program(code).run(region=self, start=start)