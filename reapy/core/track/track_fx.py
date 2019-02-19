from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class TrackFX(ReapyObject):

    _class_name = "TrackFX"
    
    def __init__(self, parent_track=None, index=None, parent_track_id=None):
        if parent_track_id is None:
            message = (
                "One of `parent_track` or `parent_track_id` must be specified."
            )
            assert parent_track is not None, message
            parent_track_id = parent_track.id
        self.track_id = parent_track_id
        self.index = index
        
    @property
    def _kwargs(self):
        return {"parent_track_id": self.track_id, "index": self.index}
        
    def close_ui(self):
        self.is_ui_open = False
        
    def copy_to_take(self, take, index=0):
        """
        Copy FX to take.
        
        Parameters
        ----------
        take : Take
            Destination take.
        index : int
            Index on destination take.
            
        See also
        --------
        TrackFX.move_to_take
        """
        RPR.TrackFX_CopyToTake(
            self.track_id, self.index, take.id, index, False
        )
        
    def copy_to_track(self, track, index=0):
        """
        Copy FX to track.
        
        Parameters
        ----------
        track : Track
            Destination track.
        index : int
            Index on destination track.
            
        See also
        --------
        TrackFX.move_to_track
        """
        RPR.TrackFX_CopyToTrack(
            self.track_id, self.index, track.id, index, False
        )
        
    def delete(self):
        """
        Delete FX.
        """
        RPR.TrackFX_Delete(self.track_id, self.index)
        
    def disable(self):
        self.is_enabled = False
        
    def enable(self):
        self.is_enabled = True
        
    @property
    def is_enabled(self):
        is_enabled = bool(RPR.TrackFX_GetEnabled(self.track_id, self.index))
        return is_enabled
        
    @is_enabled.setter
    def is_enabled(self, enabled):
        RPR.TrackFX_SetEnabled(self.track_id, self.index, enabled)
        
    @property
    def is_online(self):
        is_online = not bool(RPR.TrackFX_GetOffline(self.track_id, self.index))
        return is_online
    
    @is_online.setter   
    def is_online(self, online):
        offline = not online
        RPR.TrackFX_SetOffline(self.track_id, self.index, offline)
        
    @property
    def is_ui_open(self):
        is_ui_open = bool(RPR.TrackFX_GetOpen(self.track_id, self.index))
        return is_ui_open
        
    @is_ui_open.setter
    def is_ui_open(self, open):
        RPR.TrackFX_SetOpen(self.track_id, self.index, open)
        
    def make_offline(self):
        self.is_online = False
        
    def make_online(self):
        self.is_online = True
        
    def move_to_take(self, take, index=0):
        """
        Move FX to take.
        
        Parameters
        ----------
        take : Take
            Destination take.
        index : int
            Index on destination take.
            
        See also
        --------
        TrackFX.copy_to_take
        """
        RPR.TrackFX_CopyToTake(
            self.track_id, self.index, take.id, index, True
        )
        
    def move_to_track(self, track, index=0):
        """
        Move FX to track.
        
        Parameters
        ----------
        track : Track
            Destination track.
        index : int
            Index on destination track.
            
        See also
        --------
        TrackFX.copy_to_track
        """
        RPR.TrackFX_CopyToTrack(
            self.track_id, self.index, track.id, index, True
        )
        
    @property
    def n_params(self):
        n_params = RPR.TrackFX_GetNumParams(self.track_id, self.index)
        return n_params
        
    @property
    def name(self):
        name = RPR.TrackFX_GetFXName(self.track_id, self.index, "", 2048)[3]
        return name
        
    @property
    def parent_track(self):
        track = Track(self.track_id)
        return track
        
    @property
    def preset(self):
        preset = RPR.TrackFX_GetPreset(self.track_id, self.index, "", 2048)[3]
        return preset
        
    @preset.setter
    def preset(self, preset):
        RPR.TrackFX_SetPreset(self.track_id, self.index, preset)
        
    def open_ui(self):
        self.is_ui_open = True
        
        
from .track import Track