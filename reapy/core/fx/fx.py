"""Define FX and FXParam classes."""

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import DistError, UndefinedFXParamError
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
        if isinstance(self.parent, reapy.Track):
            prefix = "TrackFX_"
        else:
            prefix = "TakeFX_"
        functions = {
            name.replace(prefix, ""): function
            for name, function in RPR.__dict__.items()
            if name.startswith(prefix)
        }
        return functions

    @property
    def _kwargs(self):
        return {"parent_id": self.parent_id, "index": self.index}

    def close_chain(self):
        """Close FX chain."""
        self.functions["Show"](self.parent.id, self.index, 0)

    def close_floating_window(self):
        """Close FX floating window."""
        self.functions["Show"](self.parent.id, self.index, 2)

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
        track : Track
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
    def n_inputs(self):
        """
        Number of inputs of FX.

        :type: int
        """
        return self.functions["GetIOSize"](
            self.parent.id, self.index, 0, 0
        )[3]

    @property
    def n_outputs(self):
        """
        Number of outputs of FX.

        :type: int
        """
        return self.functions["GetIOSize"](
            self.parent.id, self.index, 0, 0
        )[4]

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

    def open_chain(self):
        """Open FX chain with focus on FX."""
        self.functions["Show"](self.parent.id, self.index, 1)

    def open_floating_window(self):
        """Open FX floating window."""
        self.functions["Show"](self.parent.id, self.index, 3)

    def open_ui(self):
        """Open FX user interface."""
        self.is_ui_open = True

    @property
    def params(self):
        """
        List of parameters.

        :type: FXParamsList
        """
        params = reapy.FXParamsList(self)
        return params

    @property
    def parent(self):
        """
        FX parent.

        :type: Track or Take
        """
        if self.parent_id.startswith("(MediaTrack*)"):
            return reapy.Track(self.parent_id)
        return reapy.Take(self.parent_id)

    @property
    def preset(self):
        """
        FX preset name.

        :type: str

        Attribute can be set by passing a str or int. In the first
        case, the str can either be a preset name or the path to a
        .vstpreset file. Otherwise, the int is the preset index.
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

    @property
    def window(self):
        """
        Floating window associated to FX, if it exists.

        :type: Window or NoneType
        """
        window = reapy.Window(
            self.functions["GetFloatingWindow"](self.parent.id, self.index)
        )
        if not window._is_defined:
            window = None
        return window


class FXList(ReapyObjectList):

    """
    Container class for a list of FXs.

    FXs can be accessed by name or index.

    Examples
    --------
    >>> fx_list = track.fxs
    >>> fx_list[0]
    FX(parent_id="(MediaTrack*)0x0000000006CDEBE0", index=0)
    >>> len(fx_list)
    1
    >>> fx_list["VST: ReaComp (Cockos)"]
    FX(parent_id="(MediaTrack*)0x0000000006CDEBE0", index=0)
    """

    _class_name = "FXList"

    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, i):
        with reapy.inside_reaper():
            if isinstance(i, str):
                i = self._get_fx_index(name=i)
            n_fxs = self.parent.n_fxs
        if i >= n_fxs:
            raise IndexError("{} has only {} fxs".format(self.parent, n_fxs))
        i = i % n_fxs  # Allows for negative values
        fx = FX(self.parent, i)
        return fx

    def __len__(self):
        return self.parent.n_fxs

    def _get_fx_index(self, name):
        if isinstance(self.parent, reapy.Track):
            prefix = "TrackFX_"
            args = (self.parent.id, name, False, 0)
        else:
            prefix = "TakeFX_"
            args = (self.parent.id, name, 0)
        index = getattr(RPR, prefix + "AddByName")(*args)
        if index == -1:
            raise KeyError("No FX named {}".format(name))
        return index

    @property
    def _args(self):
        return self.parent,
