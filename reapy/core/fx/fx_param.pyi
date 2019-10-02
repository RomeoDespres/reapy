import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import DistError
import typing as ty


class FXParam(float):
    """FX parameter."""
    parent_list: FXParamsList
    index: int
    functions: ty.Dict[str, ty.Dict[str, ty.Callable[..., ty.Any]]]

    def __init__(
            self, value: float, parent_list: FXParamsList, index: int,
            functions: ty.Dict[str, ty.Dict[str, ty.Callable[..., ty.Any]]]
    ) -> None:
        ...

    def __new__(self, value: float, *args: ty.Any,
                **kwargs: ty.Any) -> FXParam:
        ...

    def add_envelope(self) -> reapy.Envelope:
        """
        Create envelope for the parameter and return it.

        Returns
        -------
        envelope : Envelope
            New envelope for the parameter.

        Notes
        -----
        If the envelope already exists, the function returns it.
        """
        ...

    @property
    def envelope(self) -> ty.Optional[reapy.Envelope]:
        """
        Parameter envelope (or None if it doesn't exist).

        :type: Envelope or NoneType
        """
        ...

    def format_value(self, value: float) -> str:
        """
        Return human readable string for value.

        It is the way ``value`` would be printed in REAPER GUI if it
        was the actual parameter value. Only works with FX that
        support Cockos VST extensions.

        Parameters
        ----------
        value : float
            Value to format.

        Returns
        -------
        formatted : str
            Formatted value.
        """
        ...

    @property
    def formatted(self) -> str:
        """
        Human readable string for parameter value.

        Only works with FX that support Cockos VST extensions.

        :type: str
        """
        ...

    @property
    def name(self) -> str:
        """
        Parameter name.

        :type: str
        """
        ...

    @property
    def normalized(self) -> NormalizedFXParam:
        """
        Normalized FX parameter.

        Attribute can be set with a float, but be careful that since
        floats are immutable, this parameter won't have to right value
        anymore. See Examples below.

        :type: NormalizedFXParam

        Examples
        --------
        Say the parameter range is (0.0, 20.0).

        >>> param = fx.params[0]
        >>> param
        10.0
        >>> param.normalized
        0.5

        If you set the parameter like below, the parameter moves in
        REPAER, but the FXParam object you are using is not valid
        anymore.

        >>> param.normalized = 1
        >>> param, param.normalized
        10.0, 0.5

        You thus have to grab the updated FXParam from the FX like
        below.

        >>> param = fx.params[0]
        >>> param, param.normalized
        20.0, 1.0
        """
        ...

    @normalized.setter
    def normalized(self, value: float) -> None:
        ...

    @property
    def range(self) -> ty.Tuple[float, float]:
        """
        Parameter range.

        :type: float, float
        """
        ...


class FXParamsList(ReapyObjectList):
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
    parent_id: str
    fx_index: int
    functions: ty.Dict[str, ty.Callable[..., ty.Any]]

    def __init__(self,
                 parent_fx: ty.Optional[reapy.FX] = None,
                 parent_id: ty.Optional[str] = None,
                 parent_fx_index: ty.Optional[int] = None) -> None:
        ...

    def __getitem__(self, i: ty.Union[str, int]) -> FXParam:
        ...

    def __iter__(self) -> ty.Iterator[FXParam]:
        ...

    def __len__(self) -> int:
        ...

    def __setitem__(self, i: ty.Union[str, int], value: float) -> None:
        ...

    @reapy.inside_reaper()
    def _get_param_index(self, name: str) -> int:
        ...

    @reapy.inside_reaper()
    def _get_values(self) -> ty.List[float]:
        """Return values of all parameters in self."""
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, ty.Union[int, str]]:
        ...

    @property
    def parent_fx(self) -> reapy.FX:
        """
        Parent FX.

        :type: FX
        """
        ...


class NormalizedFXParam(FXParam):
    """
    Normalized FX parameter.

    Access it via FXParam.normalized.

    Examples
    --------
    >>> fx.params[0]
    0.0
    >>> fx.params[0].range
    (-2.0, 0.0)
    >>> fx.params[0].normalized
    1.0
    >>> fx.params[0].normalized.range
    (0.0, 1.0)
    """
    def format_value(self, value: float) -> str:
        """
        Return human readable string for value.

        It is the way ``value`` would be printed in REAPER GUI if it
        was the actual parameter value. Only works with FX that
        support Cockos VST extensions.

        Parameters
        ----------
        value : float
            Value to format.

        Returns
        -------
        formatted : str
            Formatted value.
        """
        ...

    @property
    def range(self) -> ty.Tuple[float, float]:
        """
        Parameter range (always equal to (0.0, 1.0)).
        """
        ...

    @property
    def raw(self) -> FXParam:
        """
        Raw (i.e. unnormalized) parameter.

        :type: FXParam
        """
        ...
