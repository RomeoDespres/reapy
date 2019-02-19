import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program


class Marker(ReapyObject):

    _class_name = "Marker"

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
        
    def _get_enum_index(self):
        """
        Return marker index as needed by RPR.EnumProjectMarkers2.
        """
        code = """
        index = [
            i for i, m in enumerate(project.markers)
            if m.index == marker.index
        ][0]
        """
        index = Program(code, "index").run(
            marker=self, project=reapy.Project(self.project_id)
        )[0]
        return index
     
    @property
    def _kwargs(self):
        return {
            "index": self.index, "parent_project_id": self.project_id
        }
        
    def delete(self):
        """
        Delete marker.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, False)
        
    @property
    def position(self):
        """
        Return marker position.
        
        Returns
        -------
        position : float
            Marker position in seconds.
        """
        code = """
        index = marker._get_enum_index()
        position = RPR.EnumProjectMarkers2(
            marker.project_id, index, 0, 0, 0, 0, 0
        )[4]
        """
        position = Program(code, "position").run(marker=self)[0]
        return position
        
    @position.setter
    def position(self, position):
        """
        Set marker position.
        
        Parameters
        ----------
        position : float
            Marker position in seconds.
        """
        RPR.SetProjectMarker2(self.project_id, self.index, False, position, 0, "")