import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty
from typing_extensions import TypedDict


class MarkerInfo(TypedDict):

    index: int
    enum_index: int
    project_id: str
    position: float
    name: str


class Marker(ReapyObject):

    _class_name = "Marker"
    project: reapy.Project
    project_id: int
    index: int
    enum_index: int

    def __init__(self,
                 parent_project: ty.Optional[reapy.Project] = None,
                 index: ty.Optional[int] = None,
                 parent_project_id: ty.Optional[int] = None,
                 enum_index: ty.Optional[int] = None):
        ...

    @reapy.inside_reaper()
    def _get_enum_index(self) -> int:
        """
        Return marker index as needed by RPR.EnumProjectMarkers2.
        """
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, int]:
        ...

    def delete(self) -> None:
        """
        Delete marker.
        """
        ...

    @property
    def name(self) -> str:
        """
        Marker name.

        :type: str
        """


    @name.setter
    def name(self, name: str) -> None:
        """
        Set marker name.

        Parameters
        ----------
        name : str
        """

    @property
    def position(self) -> float:
        """
        Return marker position.

        Returns
        -------
        position : float
            Marker position in seconds.
        """
        ...

    @position.setter
    def position(self, position: float) -> None:
        """
        Set marker position.

        Parameters
        ----------
        position : float
            Marker position in seconds.
        """
        ...

    @property
    def infos(self) -> MarkerInfo:
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
        ...
