import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class Region(ReapyObject):

    _class_name = "Region"
    project_id: int
    index: int

    def __init__(self,
                 parent_project: ty.Optional[reapy.Project] = None,
                 index: ty.Optional[int] = None,
                 parent_project_id: ty.Optional[int] = None) -> None:
        ...

    @reapy.inside_reaper()
    def _get_enum_index(self) -> int:
        """
        Return region index as needed by RPR.EnumProjectMarkers2.
        """
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, int]:
        ...

    def add_rendered_track(self, track: reapy.Track) -> None:
        """
        Add track to region render matrix for this region.

        Parameters
        ----------
        track : Track
            Track to add.

        See also
        --------
        Region.add_rendered_tracks
            Efficiently add several tracks to region render matrix.
        Region.remove_rendered_track
        Region.remove_rendered_tracks
        """
        ...

    @reapy.inside_reaper()
    def add_rendered_tracks(self, tracks: ty.List[reapy.Track]) -> None:
        """
        Efficiently add  several tracks to region render matrix.

        Parameters
        ----------
        tracks : list of Track
            Tracks to add.

        See also
        --------
        Region.remove_rendered_tracks
        """
        ...

    @reapy.inside_reaper()
    @property
    def end(self) -> float:
        """
        Region end.

        :type: float
            Region end in seconds.
        """
        ...

    @end.setter
    def end(self, end: float) -> None:
        """
        Set region end.

        Parameters
        ----------
        end : float
            region end in seconds.
        """
        ...

    def delete(self) -> None:
        """
        Delete region.
        """
        ...

    def remove_rendered_track(self, track: reapy.Track) -> None:
        """
        Remove track from region render matrix for this region.

        Parameters
        ----------
        track : Track
            Track to remove.

        See also
        --------
        Region.add_rendered_tracks
        Region.remove_rendered_track
        Region.remove_rendered_tracks
            Efficiently remove several tracks from render matrix.
        """
        ...

    @reapy.inside_reaper()
    def remove_rendered_tracks(self, tracks: ty.List[reapy.Track]) -> None:
        """
        Efficiently remove  several tracks from region render matrix.

        Parameters
        ----------
        tracks : list of Track
            Tracks to remove.

        See also
        --------
        Region.add_rendered_tracks
        """
        ...

    @reapy.inside_reaper()
    @property
    def rendered_tracks(self) -> ty.List[reapy.Track]:
        """
        List of tracks for this region in region render matrix.

        :type: list of Track
        """
        ...

    @reapy.inside_reaper()
    @property
    def start(self) -> float:
        """
        Region start.

        :type: float
        """
        ...

    @start.setter
    def start(self, start: float) -> None:
        """
        Set region start.

        Parameters
        ----------
        start : float
            region start in seconds.
        """
        ...
