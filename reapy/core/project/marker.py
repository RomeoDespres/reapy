import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from typing_extensions import TypedDict


class MarkerInfo(TypedDict):

    index: int
    enum_index: int
    project_id: str
    position: float
    name: str


class Marker(ReapyObject):

    _class_name = "Marker"

    def __init__(
        self, parent_project=None, index=None,
        parent_project_id=None, enum_index=None
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
            index = self.project.n_markers
        self.index = index
        if enum_index is None:
            self.enum_index = None
            enum_index = self._get_enum_index()
        self.enum_index = enum_index

    def _get_enum_index(self):
        """
        Return marker index as needed by RPR.EnumProjectMarkers2.

        Raises
        ------
        reapy.errors.UndefinedMarkerError
            Description
        """
        with reapy.inside_reaper():
            for marker in self.project.markers:
                if marker.index == self.index:
                    return marker.enum_index
        raise reapy.errors.UndefinedMarkerError(self.index)

    @property
    def _kwargs(self):
        return {
            "index": self.index,
            "parent_project_id": self.project_id,
            'enum_index': self.enum_index
        }

    def delete(self):
        """
        Delete marker.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, False)

    @reapy.inside_reaper()
    @property
    def infos(self):
        """Get all Region infos in one call.

        Returns
        -------
        RegionInfo
            index: int
            enum_index: int
            project_id: str
            position: float
            name: str
        """
        enum_index = self._get_enum_index()
        args = self.project_id, enum_index, 0, 0, 0, 0, 0
        _, _, _, _, position, _, _, index = RPR.EnumProjectMarkers2(*args)
        out: MarkerInfo = {
            'index': index,
            'enum_index': enum_index,
            'project_id': self.project_id,
            'position': position,
            'name': self.name,
        }
        return out

    @property
    def name(self):
        """
        Marker name.

        :type: str
        """
        with reapy.inside_reaper():
            # index = self._get_enum_index()
            fs = RPR.SNM_CreateFastString('0' * 1024)
            args = self.project_id, self.index, False, fs
            RPR.SNM_GetProjectMarkerName(*args)
            result = RPR.SNM_GetFastString(fs)
            RPR.SNM_DeleteFastString(fs)
        return result

    @name.setter
    def name(self, name):
        """
        Set marker name.

        Parameters
        ----------
        name : str
        """
        args = self.project_id, self.index, False, self.position, 0, name
        RPR.SetProjectMarker2(*args)

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
        print(f'enum index in position: {index}')
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
        RPR.SetProjectMarker2(
            self.project_id, self.index, False, position, 0, self.name
        )
