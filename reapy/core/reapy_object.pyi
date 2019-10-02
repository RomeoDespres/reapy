import reapy
import typing as ty
from typing_extensions import TypedDict

ReapyObjectDict = TypedDict(
    'ReapyObjectDict', {
        "__reapy__": bool,
        "class": str,
        "args": ty.Tuple[ty.Any, ...],
        "kwargs": ty.Dict[str, ty.Any]
    })


class ReapyObject:
    """Base class for reapy objects."""
    def __eq__(self, other: object) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def _args(self) -> ty.Tuple[ty.Any, ...]:
        ...

    @property
    def _is_defined(self) -> bool:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, ty.Any]:
        ...

    def _to_dict(self) -> ReapyObjectDict:
        ...


class ReapyObjectList(ReapyObject):
    """Abstract class for list of ReapyObjects."""

    pass
