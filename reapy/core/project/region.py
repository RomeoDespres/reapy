import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Region(ReapyObject):

    _class_name = "Region"

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

    @reapy.inside_reaper()
    def _get_enum_index(self):
        """
        Return region index as needed by RPR.EnumProjectMarkers2.
        """
        return next(
            i for i, r in enumerate(reapy.Project(self.project_id).regions)
            if r.index == region.index
        )

    @property
    def _kwargs(self):
        return {
            "index": self.index, "parent_project_id": self.project_id
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
        args = self.project_id, self.index, True, self.start, end, ""
        RPR.SetProjectMarker2(*args)

    def delete(self):
        """
        Delete region.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, True)

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
            self.project_id, self.index, 1, start, self.end, ""
        )
