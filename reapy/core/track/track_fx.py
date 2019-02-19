from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.errors import UndefinedFXParamError
from reapy.tools import Program


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
    def n_presets(self):
        n_presets = RPR.TrackFX_GetPresetIndex(
            self.track_id, self.index, 0
        )[-1]
        return n_presets
        
    @property
    def name(self):
        name = RPR.TrackFX_GetFXName(self.track_id, self.index, "", 2048)[3]
        return name
            
    def open_ui(self):
        self.is_ui_open = True
        
    @property
    def params(self):
        params = TrackFXParamsList(self)
        return params
        
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
        """
        Set FX preset.
        
        Parameters
        ----------
        preset : str or int
            If str, preset name or path to .vstpreset file. If int,
            preset index. Set to -2 for factory preset, and -1 for user
            default preset.
        """
        if isinstance(preset, str):
            RPR.TrackFX_SetPreset(self.track_id, self.index, preset)
        elif isinstance(preset, int):
            RPR.TrackFX_SetPresetByIndex(self.track_id, self.index, preset)
        
    @property
    def preset_index(self):
        index = RPR.TrackFX_GetPresetIndex(self.track_id, self.index, 0)[0]
        return index
    
    @property
    def preset_file(self):
        file = RPR.TrackFX_GetUserPresetFilename(
            self.track_id, self.index, "", 2048
        )[2]
        return file
        
    def use_previous_preset(self):
        RPR.TrackFX_NavigatePresets(self.track_id, self.index, -1)
        
    def use_next_preset(self):
        RPR.TrackFX_NavigatePresets(self.track_id, self.index, 1)
        
class TrackFXParam(float):    

    @property
    def name(self):
        l = self.parent_list
        name = RPR.TrackFX_GetParamName(
            l.track_id, l.fx_index, self.index, "", 2048
        )[4]
        return name
        
    @property
    def range(self):
        l = self.parent_list
        min, max = RPR.TrackFX_GetParam(
            l.track_id, l.fx_index, self.index, 0, 0
        )[-2:]
        return min, max
        
class TrackFXParamsList(ReapyObject):

    _class_name = "TrackFXParamsList"
    
    def __init__(
        self, parent_fx=None, parent_track_id=None, parent_fx_index=None
    ):
        if parent_fx_index is None:
            parent_fx_index = parent_fx.index
        if parent_track_id is None:
            parent_track_id = parent_fx.track_id
        self.track_id = parent_track_id
        self.fx_index = parent_fx_index
        
    def __getitem__(self, i):
        if isinstance(i, str):
            i = self._get_param_index(i)
        value = RPR.TrackFX_GetParam(self.track_id, self.fx_index, i, 0, 0)[0]
        param = TrackFXParam(value)
        param.parent_list = self
        param.index = i
        return param
        
    def __len__(self):
        length = self.parent_fx.n_params
        return length
        
    def __setitem__(self, i, value):
        if isinstance(i, str):
            i = self._get_param_index(i)
        RPR.TrackFX_SetParam(self.track_id, self.fx_index, i, value)
        
    def _get_param_index(self, name):
        code = """
        names = [l[i].name for i in range(len(l))]
        try:
            index = names.index(name)
        except ValueError:
            index = -1
        """
        index = Program(code, "index").run(name=name, l=self)[0]
        if index == -1:
            raise UndefinedFXParamError(self.parent_fx.name, name)
        return index
    
    @property
    def _kwargs(self):
        return {
            "parent_fx_index": self.fx_index, "parent_track_id": self.track_id
        }
        
    @property
    def parent_fx(self):
        fx = TrackFX(parent_track_id=self.track_id, index=self.fx_index)
        return fx
        
        
from .track import Track