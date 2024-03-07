import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Marker(ReapyObject):

    _class_name = "Marker"
    _name = "NAME_ME"
    user_id = None

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
        self.project = reapy.Project(parent_project_id)
        self.project_id = parent_project_id
        if index is None:
            index = len(self.project.markers)
        self.index = index

    @reapy.inside_reaper()
    def _get_enum_index(self):
        """
        Return marker index as needed by RPR.EnumProjectMarkers2.
        """
        return self.index
        # for index, marker in enumerate(self.project.markers):
        #     if marker.index == self.index:
        #         return index

    @property
    def _kwargs(self):
        return {
            "index": self.index, "parent_project_id": self.project_id
        }

    def delete(self):
        """
        Delete marker.
        """
        RPR.DeleteProjectMarker(self.project_id, self.user_id, False)

    @reapy.inside_reaper()
    @property
    def position(self):
        """
        Return marker position.

        Returns
        -------
        position : float
            Marker position in seconds.
        """
        index = self._get_enum_index()
        return RPR.EnumProjectMarkers2(self.project_id, index, 0, 0, 0, 0, 0)[4]

    @position.setter
    def position(self, position):
        """
        Set marker position.

        Parameters
        ----------
        position : float
            Marker position in seconds.
        """
        self._position = position
        RPR.SetProjectMarker2(
            self.project_id, self.index, False, position, 0,self._name
        )

  
    def user_id(self):
        """
        Return marker position.

        Returns
        -------
        position : float
            Marker position in seconds.
        """
        index = self._get_enum_index()
        return RPR.EnumProjectMarkers2(self.project_id, index, 0, 0, 0, 0, 0)[7]

    @reapy.inside_reaper()
    @property
    def name(self):
        """
        Return the marker label

        THAT IS NOT WORKING ATM THEREFORE WILL RETURN AN EMPTY STRING 

        Returns
        -------
        position : float
            Marker position in seconds.
        """
        return ""



    @name.setter
    def name(self, name: str) -> None: 
        self._name = name
        RPR.SetProjectMarker2(self.project_id, self.user_id(), False, self.position, 0, name)