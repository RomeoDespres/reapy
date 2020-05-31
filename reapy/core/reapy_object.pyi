import reapy
import typing as ty
from typing_extensions import TypedDict

ReapyObjectDict = TypedDict(
    'ReapyObjectDict', {
        "__reapy__": bool,
        "module": bool,
        "class": str,
        "args": ty.Tuple[object, ...],
        "kwargs": ty.Dict[str, object],
        "state": ty.Optional[ty.Dict[str, object]]
    }
)


class ReapyObject:
    """Base class for reapy objects."""

    def __eq__(self, other: object) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def _args(self) -> ty.Tuple[object, ...]:
        ...

    @property
    def _is_defined(self) -> bool:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, object]:
        ...

    @property
    def _state(self) -> ty.Optional[ty.Dict[str, object]]:
        ...

    @_state.setter
    def _state(self, state: ty.Optional[ty.Dict[str, object]]) -> None: ...

    def _to_dict(self) -> ReapyObjectDict:
        ...

    def map(
        self,
        method_name: str,
        iterables: ty.Dict[str, object],
        defaults: ty.Optional[ty.Dict[str, object]] = None
    ) -> ty.List[object]:
        """
        Perform object method among iterables inside reaper.

        Note
        ----
        Opposite to `inside_reaper`, which saves on deferred executions,
        map saves on socket connections, so, basically, if you have complex
        code needs to be performed at one deferred call — use `inside_reaper`,
        if large amount of data has to be proceed within particular method —
        use `object.map()`.

        Parameters
        ----------
        method_name : str
            name of the object method (self)
        iterables : Dict[str, List[jsonable]]
            str is argument name, List for mapping
        defaults : Dict[str, jsonable]
            partial arguments, that won't be changed though iteration

        Returns
        -------
        List[<method result>]

        Example
        -------
        import reapy as rpr
        take = rpr.Project().selected_items[0].active_take

        @rpr.inside_reaper()
        def test():
            for i in [6.0] * 1000000:
                take.time_to_ppq(6.0)


        def test_map():
            take.map('time_to_ppq', iterables={'time': [6.0] * 1000000})


        test()      # runs 140s
        test_map()  # runs 12s as from outside as from inside
        """
        ...


class ReapyObjectList(ReapyObject):
    """Abstract class for list of ReapyObjects."""

    pass
