import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program

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
        code = """
        for track in tracks:
            region.add_rendered_track(track)
        """
        Program(code).run(region=self, tracks=tracks)
        
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
        code = """
        for track in tracks:
            region.remove_rendered_track(track)
        """
        Program(code).run(region=self, tracks=tracks)
    
    @property    
    def rendered_tracks(self):
        """
        Return list of tracks for this region in region render matrix.
        
        Returns
        -------
        rendered_tracks : list of Track
            List of tracks for this region in region render matrix.
        """
        code = """
        i = 0
        tracks = []
        while i == 0 or tracks[-1]._is_defined:
            track_id = RPR.EnumRegionRenderMatrix(
                region.project_id, region.index, i
            )
            tracks.append(reapy.Track(track_id))
            i += 1
        tracks = tracks[:-1]
        """
        rendered_tracks = Program(code, "tracks").run(region=self)[0]
        return rendered_tracks
        
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
        
        
from ..track.track import Track