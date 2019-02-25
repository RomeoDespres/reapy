import reapy
from reapy.core import ReapyObject
from reapy.errors import DistError


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

    """
    Container class for a list of FX parameters.

    Parameters can be accessed by name or index.

    Examples
    --------
    >>> params_list = fx.params
    >>> params_list[0]  # Say this is "Dry Gain" parameter
    0.5
    >>> params_list["Dry Gain"]
    0.5
    >>> params_list["Dry Gain"] = 0.1
    >>> params_list[0]
    0.1
    """

    _class_name = "FXParamsList"

    def __init__(
        self, parent_fx=None, parent_id=None, parent_fx_index=None
    ):
        if parent_fx is None:
            parent_fx = reapy.FX(parent_id=parent_id, index=parent_fx_index)
        self.parent_id = parent_fx.parent_id
        self.fx_index = parent_fx.index
        self.functions = parent_fx.functions

    def __getitem__(self, i):
        with reapy.inside_reaper():
            if isinstance(i, str):
                i = self._get_param_index(i)
            n_params = len(self)
            if i >= n_params:
                raise IndexError(
                    "{} has only {} params".format(self.parent_fx, n_params)
                )
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
        with reapy.inside_reaper():
            if isinstance(i, str):
                i = self._get_param_index(i)
            n_params = len(self)
            if i >= n_params:
                raise IndexError(
                    "{} has only {} params".format(self.parent_fx, n_params)
                )
        self.functions["SetParam"](
            self.parent_id, self.fx_index, i, value
        )

    def _get_param_index(self, name):
        code = """
        names = [param_list[i].name for i in range(len(param_list))]
        index = names.index(name)
        """
        try:
            index = Program(code, "index").run(
                name=name, param_list=self
            )[0]
            return index
        except DistError:
            raise IndexError(
                "{} has no param named {}".format(self.parent_fx, name)
            )

    @property
    def _kwargs(self):
        return {
            "parent_fx_index": self.fx_index, "parent_id": self.parent_id
        }

    @property
    def parent_fx(self):
        """
        Parent FX.

        :type: FX
        """
        fx = reapy.FX(parent_id=self.parent_id, index=self.fx_index)
        return fx
