import reapy
from reapy.core import ReapyObject
import reapy.reascript_api as RPR
import typing as ty


class Window(ReapyObject):
    id: bytes

    def __init__(self, id: bytes) -> None:
        ...

    @property
    def _args(self) -> ty.Tuple[bytes]:
        ...

    def refresh(self) -> None:
        """Refresh window."""
        ...
