"""Define FX and FXParam classes."""

from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.errors import UndefinedFXParamError
from reapy.tools import Program


class FX(ReapyObject):

    """FX on a Track or a Take."""

    _class_name = "FX"

    def __init__(self, parent=None, index=None, parent_id=None):
        if parent_id is None:
            message = (
                "One of `parent` or `parent_id` must be specified."
            )
            assert parent is not None, message
            parent_id = parent.id
        self.parent_id = parent_id
        self.index = index
        self.functions = self._get_functions()

    def _get_functions(self):
        function_names = [
            "AddByName",
            "CopyToTake",
            "CopyToTrack",
            "Delete",
            "EndParamEdit",
            "FormatParamValue",
            "FormatParamValueNormalized",
            "GetByName",
            "GetChainVisible",
            "GetCount",
            "GetEnabled",
            "GetEQ",
            "GetEQBandEnabled",
            "GetEQParam",
            "GetFloatingWindow",
            "GetFormattedParamValue",
            "GetFXGUID",
            "GetFXName",
            "GetInstrument",
            "GetIOSize",
            "GetNamedConfigParm",
            "GetNumParams",
            "GetOffline",
            "GetOpen",
            "GetParam",
            "GetParameterStepSizes",
            "GetParamEx",
            "GetParamName",
            "GetParamNormalized",
            "GetPinMappings",
            "GetPreset",
            "GetPresetIndex",
            "GetRecChainVisible",
            "GetRecCount",
            "GetUserPresetFilename",
            "NavigatePresets",
            "SetEnabled",
            "SetEQBandEnabled",
            "SetEQParam",
            "SetNamedConfigParm",
            "SetOffline",
            "SetOpen",
            "SetParam",
            "SetParamNormalized",
            "SetPinMappings",
            "SetPreset",
            "SetPresetByIndex",
            "Show"
        ]
        if self.parent_id.startswith("(MediaTrack*)"):
            fx_type = "TrackFX"
        else:
            fx_type = "TakeFX"
        functions = {
            name: getattr(RPR, "{}_{}".format(fx_type, name))
            for name in function_names
        }
        return functions

    @property
    def _kwargs(self):
        return {"parent_id": self.parent_id, "index": self.index}

    def close_ui(self):
        """Close user interface."""
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
        FX.move_to_take
        """
        self.functions["CopyToTake"](
            self.parent_id, self.index, take.id, index, False
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
        FX.move_to_track
        """
        self.functions["CopyToTrack"](
            self.parent_id, self.index, track.id, index, False
        )

    def delete(self):
        """Delete FX."""
        self.functions["Delete"](self.parent_id, self.index)

    def disable(self):
        """Disable FX."""
        self.is_enabled = False

    def enable(self):
        """Enable FX."""
        self.is_enabled = True

    @property
    def is_enabled(self):
        """
        Whether FX is enabled.

        :type: bool
        """
        is_enabled = bool(
            self.functions["GetEnabled"](self.parent_id, self.index)
        )
        return is_enabled

    @is_enabled.setter
    def is_enabled(self, enabled):
        self.functions["SetEnabled"](self.parent_id, self.index, enabled)

    @property
    def is_online(self):
        """
        Whether FX is online.

        :type: bool
        """
        is_online = not bool(
            self.functions["GetOffline"](self.parent_id, self.index)
        )
        return is_online

    @is_online.setter
    def is_online(self, online):
        offline = not online
        self.functions["SetOffline"](self.parent_id, self.index, offline)

    @property
    def is_ui_open(self):
        """
        Whether FX user interface is open.

        :type: bool
        """
        is_ui_open = bool(
            self.functions["GetOpen"](self.parent_id, self.index)
        )
        return is_ui_open

    @is_ui_open.setter
    def is_ui_open(self, open):
        self.functions["SetOpen"](self.parent_id, self.index, open)

    def make_offline(self):
        """Make FX offline."""
        self.is_online = False

    def make_online(self):
        """Make FX online."""
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
        FX.copy_to_take
        """
        self.functions["CopyToTake"](
            self.parent_id, self.index, take.id, index, True
        )

    def move_to_track(self, track, index=0):
        """
        Move FX to track.

        Parameters
        ----------
        track : reapy.Track
            Destination track.
        index : int
            Index on destination track.

        See also
        --------
        FX.copy_to_track
        """
        self.functions["CopyToTrack"](
            self.parent_id, self.index, track.id, index, True
        )

    @property
    def n_params(self):
        """
        Number of parameters.

        :type: int
        """
        n_params = self.functions["GetNumParams"](self.parent_id, self.index)
        return n_params

    @property
    def n_presets(self):
        """
        Number of presets.

        :type: int
        """
        n_presets = self.functions["GetPresetIndex"](
            self.parent_id, self.index, 0
        )[-1]
        return n_presets

    @property
    def name(self):
        """
        FX name.

        :type: str
        """
        name = self.functions["GetFXName"](
            self.parent_id, self.index, "", 2048
        )[3]
        return name

    def open_ui(self):
        """Open FX user interface."""
        self.is_ui_open = True

    @property
    def params(self):
        """
        List of parameters.

        :type: FXParamsList
        """
        params = FXParamsList(self)
        return params

    @property
    def parent_track(self):
        """
        FX parent track.

        :type: reapy.Track
        """
        track = Track(self.parent_id)
        return track

    @property
    def preset(self):
        """
        FX preset name.

        :type: str
        """
        preset = self.functions["GetPreset"](
            self.parent_id, self.index, "", 2048
        )[3]
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
            self.functions["SetPreset"](
                self.parent_id, self.index, preset
            )
        elif isinstance(preset, int):
            self.functions["SetPresetByIndex"](
                self.parent_id, self.index, preset
            )

    @property
    def preset_index(self):
        """
        FX preset index.

        :type: int
        """
        index = self.functions["GetPresetIndex"](
            self.parent_id, self.index, 0
        )[0]
        return index

    @property
    def preset_file(self):
        """
        Path to FX preset file.

        :type: str
        """
        file = self.functions["GetUserPresetFilename"](
            self.parent_id, self.index, "", 2048
        )[2]
        return file

    def use_previous_preset(self):
        """Use previous preset in the presets list."""
        self.functions["NavigatePresets"](self.parent_id, self.index, -1)

    def use_next_preset(self):
        """Use next preset in the presets list."""
        self.functions["NavigatePresets"](self.parent_id, self.index, 1)


class FXParam(float):

    """FX parameter."""

    @property
    def name(self):
        """
        Parameter name.

        :type: str
        """
        parent_list = self.parent_list
        name = self.functions["GetParamName"](
            parent_list.parent_id, parent_list.fx_index, self.index, "", 2048
        )[4]
        return name

    @property
    def range(self):
        """
        Parameter range.

        :type: float, float
        """
        parent_list = self.parent_list
        min, max = self.functions["GetParam"](
            parent_list.parent_id, parent_list.fx_index, self.index, 0, 0
        )[-2:]
        return min, max


class FXParamsList(ReapyObject):

    _class_name = "FXParamsList"

    def __init__(
        self, parent_fx=None, parent_id=None, parent_fx_index=None
    ):
        if parent_fx is None:
            parent_fx = FX(parent_id=parent_id, index=parent_fx_index)
        self.parent_id = parent_fx.parent_id
        self.fx_index = parent_fx.index
        self.functions = parent_fx.functions

    def __getitem__(self, i):
        if isinstance(i, str):
            i = self._get_param_index(i)
        value = self.functions["GetParam"](
            self.parent_id, self.fx_index, i, 0, 0
        )[0]
        param = FXParam(value)
        param.parent_list = self
        param.index = i
        param.functions = self.functions
        return param

    def __len__(self):
        length = self.parent_fx.n_params
        return length

    def __setitem__(self, i, value):
        if isinstance(i, str):
            i = self._get_param_index(i)
        self.functions["SetParam"](
            self.parent_id, self.fx_index, i, value
        )

    def _get_param_index(self, name):
        code = """
        names = [param_list[i].name for i in range(len(param_list))]
        try:
            index = names.index(name)
        except ValueError:
            index = -1
        """
        index = Program(code, "index").run(name=name, param_list=self)[0]
        if index == -1:
            raise UndefinedFXParamError(self.parent_fx.name, name)
        return index

    @property
    def _kwargs(self):
        return {
            "parent_fx_index": self.fx_index, "parent_id": self.parent_id
        }

    @property
    def parent_fx(self):
        """
        Parent FX.

        :type: reapy.FX
        """
        fx = FX(parent_id=self.parent_id, index=self.fx_index)
        return fx
