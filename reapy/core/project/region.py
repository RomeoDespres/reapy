from typing_extensions import TypedDict
from typing import List
import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class RegionInfo(TypedDict):
    index: int
    enum_index: int
    project_id: str
    name: str
    start: float
    end: float
    rendered_tracks: List['reapy.Track']


class Region(ReapyObject):

    _class_name = "Region"

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
            if enum_index is None:
                index = len(self.project.regions)
            else:
                index = RPR.EnumProjectMarkers2(
                    self.project_id, enum_index, 0, 0, 0, 0, 0
                )[7]
        self.index = index
        if enum_index is None:
            enum_index = self._get_enum_index()
        self.enum_index = enum_index

    @reapy.inside_reaper()
    def _get_enum_index(self):
        """
        Return region index as needed by RPR.EnumProjectMarkers2.

        Raises
        ------
        reapy.errors.UndefinedRegionError
        """
        for region in self.project.regions:
            if region.index == self.index:
                return region.enum_index
        raise reapy.errors.UndefinedRegionError(self.index)

    @property
    def _kwargs(self):
        return {
            "index": self.index, "parent_project_id": self.project_id,
            "enum_index": self.enum_index
        }

    def add_rendered_track(self, track):
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
        RPR.SetRegionRenderMatrix(self.project_id, self.index, track.id, 1)

    @reapy.inside_reaper()
    def add_rendered_tracks(self, tracks):
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
        for track in tracks:
            self.add_rendered_track(track)

    @reapy.inside_reaper()
    @property
    def end(self):
        """
        Region end.

        :type: float
            Region end in seconds.
        """
        index = self._get_enum_index()
        args = self.project_id, index, 0, 0, 0, 0, 0
        return RPR.EnumProjectMarkers2(*args)[5]

    @end.setter
    def end(self, end):
        """
        Set region end.

        Parameters
        ----------
        end : float
            region end in seconds.
        """
        args = self.project_id, self.index, True, self.start, end, self.name
        RPR.SetProjectMarker2(*args)

    def delete(self):
        """
        Delete region.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, True)

    @reapy.inside_reaper()
    @property
    def name(self):
        """
        Region name.

        :type: str
        """
        # index = self._get_enum_index()
        fs = RPR.SNM_CreateFastString('0' * 1024)
        args = self.project_id, self.index, True, fs
        RPR.SNM_GetProjectMarkerName(*args)
        result = RPR.SNM_GetFastString(fs)
        RPR.SNM_DeleteFastString(fs)
        return result

    @name.setter
    def name(self, name):
        """
        Set region name.

        Parameters
        ----------
        name : str
        """
        args = self.project_id, self.index, True, self.start, self.end, name
        RPR.SetProjectMarker2(*args)

    def remove_rendered_track(self, track):
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
        RPR.SetRegionRenderMatrix(self.project_id, self.index, track.id, -1)

    @reapy.inside_reaper()
    def remove_rendered_tracks(self, tracks):
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
        for track in tracks:
            self.remove_rendered_track(track)

    @reapy.inside_reaper()
    @property
    def rendered_tracks(self):
        """
        List of tracks for this region in region render matrix.

        :type: list of Track
        """
        i = 0
        tracks = []
        while i == 0 or tracks[-1]._is_defined:
            track_id = RPR.EnumRegionRenderMatrix(
                self.project_id, self.index, i
            )
            tracks.append(reapy.Track(track_id))
            i += 1
        return tracks[:-1]

    @reapy.inside_reaper()
    @property
    def start(self):
        """
        Region start.

        :type: float
        """
        args = self.project_id, self._get_enum_index(), 0, 0, 0, 0, 0
        return RPR.EnumProjectMarkers2(*args)[4]

    @start.setter
    def start(self, start):
        """
        Set region start.

        Parameters
        ----------
        start : float
            region start in seconds.
        """
        RPR.SetProjectMarker2(
            self.project_id, self.index, 1, start, self.end, self.name
        )

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
            name: str
            start: float
            end: float
            rendered_tracks: List[reapy.Track]
        """
        enum_index = self._get_enum_index()
        args = self.project_id, enum_index, 0, 0, 0, 0, 0
        _, _, _, _, start, end, _, index = RPR.EnumProjectMarkers2(*args)
        out: RegionInfo = {
            'index': index,
            'enum_index': enum_index,
            'project_id': self.project_id,
            'start': start,
            'end': end,
            'name': self.name,
            'rendered_tracks': self.rendered_tracks
        }
        return out
