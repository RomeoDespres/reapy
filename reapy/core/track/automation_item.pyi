from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy import Envelope
import typing as ty
from typing_extensions import TypedDict


class AutomationItem(ReapyObject):

    _class_name = "AutomationItem"
    envelope_id: int
    index: int

    def __init__(self,
                 envelope: ty.Optional[Envelope] = None,
                 index: int = 0,
                 envelope_id: ty.Optional[int] = None) -> None:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, int]:
        ...

    def delete_points_in_range(self, start: float, end: float) -> None:
        """
        Delete points between `start` and `end`.

        Parameters
        ----------
        start : float
            Range start in seconds.
        end : float
            Range end in seconds.
        """
        ...

    @property
    def length(self) -> float:
        """
        Return item length in seconds.

        Returns
        -------
        length : float
            Item length in seconds.
        """
        ...

    @length.setter
    def length(self, length: float) -> None:
        """
        Set item length.

        Parameters
        ----------
        length : float
            New item length in seconds.
        """
        ...

    @property
    def n_points(self) -> int:
        """
        Return number of automation points in item.

        Returns
        -------
        n_points : int
            Number of automation points in item.
        """
        ...

    @property
    def pool(self) -> int:
        """
        Return item pool.

        Returns
        -------
        pool : int
            Item pool.
        """
        ...

    @pool.setter
    def pool(self, pool: int) -> None:
        """
        Set item pool.

        Parameters
        ----------
        pool : int
            New item pool.
        """
        ...

    @property
    def position(self) -> float:
        """
        Return item position in seconds.

        Returns
        -------
        position : float
            Item position in seconds.
        """
        ...

    @position.setter
    def position(self, position: float) -> None:
        """
        Set item position.

        Parameters
        ----------
        position : float
            New item position in seconds.
        """
        ...
