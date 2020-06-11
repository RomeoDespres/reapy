import typing as ty

from reapy.core import ReapyObject
from reapy import reascript_api as RPR


class Coordinates(ReapyObject):
    """Keeps Swell coordinates.

    Note
    ----
    On MacOS (Darwin) root point is left bottom corner and positive y is upper.
    """

    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        self.left, self.top, self.right, self.bottom = left, top, right, bottom

    @property
    def _args(self) -> ty.Tuple[int, int, int, int]:
        return self.left, self.top, self.right, self.bottom

    def __getitem__(self, index: int) -> int:
        return self._args[index]

    def __iter__(self) -> ty.Iterator[int]:
        return (i for i in (self.left, self.top, self.right, self.bottom))

    @property
    def t(self) -> ty.Tuple[int, int, int, int]:
        """Get as Tuple.

        :type: Tuple[int, int, int, int]
            l, t, r, b
        """
        return self._args

    def max(
        self, other: ty.Union['Coordinates', ty.Tuple[int, int, int, int]]
    ) -> 'Coordinates':
        """Get rectangle of combined size of self and other.

        Note
        ----
        Rectangle is calculated respective to platform specification
        e.g. if (0,0) is bottom left — it is counted. But be afraid of
        combining screen coordinates with local coordinates.

        Parameters
        ----------
        other : ty.Union['Coordinates', ty.Tuple[int, int, int, int]]
            l, t, r, b
        """
        tmf = min
        bmf = max
        if self.bottom - self.top < 0:
            tmf = max
            bmf = min
        lm = min(self.left, other[0])
        tm = tmf(self.top, other[1])
        rm = max(self.right, other[2])
        bm = bmf(self.bottom, other[3])
        return Coordinates(lm, tm, rm, bm)

    @staticmethod
    def from_dimentions(dim: 'Dimentions') -> 'Coordinates':
        return Coordinates(dim.x, dim.y, dim.x + dim.width, dim.y + dim.height)


class Dimentions(ReapyObject):

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height

    @property
    def _args(self) -> ty.Tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height

    def __iter__(self) -> ty.Iterator[int]:
        return (i for i in (self.x, self.y, self.width, self.height))

    @property
    def t(self) -> ty.Tuple[int, int, int, int]:
        """Get as Tuple.

        :type: Tuple[int, int, int, int]
            l, t, w, h
        """
        return self._args

    @staticmethod
    def from_coordinates(coords: 'Coordinates') -> 'Dimentions':
        """Make Dimentions from Coordinates.

        Note
        ----
        If they are screen coordinates and top and bottom are flipped
        (e.g. MacOS) — It is counted. But be afraid of using such dimentions
        inside local coordinates.

        Parameters
        ----------
        coords : Coordinates

        Returns
        -------
        Dimentions
        """
        if coords.bottom - coords.top < 0:
            height = coords.top - coords.bottom
        else:
            height = coords.bottom - coords.top
        return Dimentions(
            coords.left, coords.top, coords.right - coords.left, height
        )


class Point(ReapyObject):

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    @property
    def _args(self) -> ty.Tuple[int, int]:
        return self.x, self.y

    def __iter__(self) -> ty.Iterator[int]:
        return (i for i in (self.x, self.y))

    @property
    def t(self) -> ty.Tuple[int, int]:
        """Get as Tuple.

        :type: Tuple[int, int]
            x, y
        """
        return self._args

    @staticmethod
    def from_dimentions(dimentions: Dimentions) -> 'Point':
        return Point(dimentions.x, dimentions.y)

    @staticmethod
    def from_coordinates(coords: Coordinates) -> 'Point':
        return Point.from_dimentions(Dimentions.from_coordinates(coords))


class Size(ReapyObject):

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height

    @property
    def _args(self) -> ty.Tuple[int, int]:
        return self.width, self.height

    def __iter__(self) -> ty.Iterator[int]:
        return (i for i in (self.width, self.height))

    @property
    def t(self) -> ty.Tuple[int, int]:
        """Get as Tuple.

        :type: Tuple[int, int]
            x, y
        """
        return self._args

    @staticmethod
    def from_dimentions(dimentions: Dimentions) -> 'Size':
        return Size(dimentions.width, dimentions.height)

    @staticmethod
    def from_coordinates(coords: Coordinates) -> 'Size':
        return Size.from_dimentions(Dimentions.from_coordinates(coords))


def mouse_pos() -> Point:
    """Mouse position at screen.

    Note
    ----
    I'm not sure if it should and how to return normalized value
    e.g. invert top and bottom on MacOS

    Returns
    -------
    ty.Tuple[int, int]
    """
    return Point(*RPR.GetMousePosition(0, 0))  # type:ignore
