import typing as ty
from enum import Enum

import reapy
from . import JS
from reapy.core import ReapyObject, ReapyObjectList
from reapy.errors import ResourceLoadError
from .misc import Dimentions, Coordinates, Point, Size
from .swell_translations import WS


class WindowInfo(Enum):
    USERDATA = "USERDATA"
    WNDPROC = "WNDPROC"
    DLGPROC = "DLGPROC"
    ID = "ID"
    EXSTYLE = "EXSTYLE"
    STYLE = "STYLE"

    def __str__(self) -> str:
        return ty.cast(str, self.value)


class Window(ReapyObject):

    def __init__(
        self,
        ptr: ty.Optional[JS.VoidPtr] = None,
        dimentions: Dimentions = Dimentions(0, 0, 100, 100),
        title: str = '',
        class_name: str = 'ReapyWindow',
        style: ty.Optional[ty.Union[str, WS]] = None,
    ) -> None:
        if isinstance(style, WS):
            style = hex(style.value)
        self.ptr = ptr if ptr else JS.Window_Create(
            title, class_name, *dimentions.t, styleOptional=style
        )
        if int(self.ptr) == 0:
            raise RuntimeError('window hasnt been connected')

    @property
    def _args(self) -> ty.Tuple[ty.Optional[JS.VoidPtr], Dimentions, str, str]:
        return self.ptr, self.dimentions, self.title, self.class_name

    @reapy.inside_reaper()
    def add_child(
        self,
        dimentions: Dimentions = Dimentions(10, 10, 50, 50),
        title: str = '',
    ) -> 'Window':
        wnd = Window(
            dimentions=dimentions, title=title, class_name=self.class_name
        )
        JS.Window_SetParent(wnd.ptr, self.ptr)
        wnd.position = Point.from_dimentions(dimentions)
        return wnd

    @property
    def class_name(self) -> str:
        return JS.Window_GetClassName(self.ptr, 30)

    def cleanup(self) -> None:
        JS.Window_Destroy(self.ptr)

    @property
    def childs(self) -> ty.Iterator['Window']:
        ret, array = JS.Window_ArrayAllChildEx(self.ptr, size=1000)
        if ret < 0:
            raise ResourceLoadError('c-binding exited with %s' % ret)
        for hwnd in JS.reaper_array_to_hwnd(array):
            yield Window(hwnd)

    @property
    def dimentions(self) -> Dimentions:
        return Dimentions.from_coordinates(
            Coordinates(*JS.Window_GetRect(self.ptr)[1:])
        )

    @dimentions.setter
    def dimentions(self, dimentions: Dimentions) -> None:
        c = Coordinates.from_dimentions(dimentions)
        JS.Window_SetPosition(self.ptr, *c.t)

    def get_long_int(self, info: ty.Union[str, WindowInfo]) -> int:
        return int(JS.Window_GetLong(self.ptr, str(info)))

    def get_long_ptr(self, info: ty.Union[str, WindowInfo]) -> JS.VoidPtr:
        return JS.Window_GetLongPtr(self.ptr, str(info))

    @property
    def parent(self) -> 'Window':
        ptr = JS.Window_GetParent(self.ptr)
        if int(ptr) == 0:
            raise RuntimeError('{} does not have parent'.format(self))
        return Window(ptr=ptr)

    @parent.setter
    def parent(self, other: ty.Union['Window', JS.VoidPtr]) -> None:
        if isinstance(other, Window):
            other = other.ptr
        JS.Window_SetParent(self.ptr, other)

    @property
    def position(self) -> Point:
        return Point(*JS.Window_GetRect(self.ptr)[1:3])

    @position.setter
    def position(self, pos: Point) -> None:
        JS.Mouse_SetPosition(*pos.t)

    @property
    def size(self) -> Size:
        return Size.from_coordinates(
            Coordinates(*JS.Window_GetRect(self.ptr)[1:])
        )

    @size.setter
    def size(self, size: Size) -> None:
        JS.Window_Resize(self.ptr, *size.t)

    def set_long_int(
        self, info: ty.Union[str, WindowInfo], value: int
    ) -> float:
        return JS.Window_SetLong(self.ptr, str(info), value)

    @property
    def style(self) -> WS:
        return WS(self.get_long_int('STYLE'))

    @style.setter
    def style(self, style: ty.Union[str, WS]) -> None:
        if isinstance(style, str):
            JS.Window_SetStyle(self.ptr, style)
            return
        self.set_long_int('STYLE', int(style))

    @property
    def title(self) -> str:
        return JS.Window_GetTitle(self.ptr, 300)

    @title.setter
    def title(self, title: str) -> None:
        JS.Window_SetTitle(self.ptr, title)
