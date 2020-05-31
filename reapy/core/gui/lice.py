"""Flexible wrappers for JS.LICE functionality."""
import typing as ty
import enum

import reapy
from . import JS
from reapy.core import ReapyObject
from reapy.errors import ResourceLoadError
from .misc import Coordinates, Dimentions, Point
from .window_ex import Window


class Mix(enum.Enum):
    """LICE mix modes."""

    copy: str = 'COPY'
    add: str = 'ADD'
    dodge: str = "DODGE"
    mul: str = "MUL"
    overlay: str = "OVERLAY"
    hsv_adj: str = "HSVADJ"
    mask: str = 'MASK'
    alpha: str = 'ALPHA'

    def __or__(self, other: 'Mix') -> str:
        if self.value == 'ALPHA' or other.value == 'ALPHA':
            return ''.join((self.value, other.value))
        raise TypeError("can combine only with 'ALPHA'")

    def __str__(self) -> str:
        return self.value  # type:ignore


class MixBlit(enum.Enum):
    """Extended LICE modes for blit operations."""

    copy: str = 'COPY'
    add: str = 'ADD'
    dodge: str = "DODGE"
    mul: str = "MUL"
    overlay: str = "OVERLAY"
    hsv_adj: str = "HSVADJ"
    mask: str = 'MASK'
    alpha: str = 'ALPHA'
    blur: str = 'BLUR'
    alpha_mul: str = 'ALPHAMUL'

    @staticmethod
    def chan_copy(ch1: str, ch2: str) -> str:
        """Copy channel 1 to channel 2.

        Parameters
        ----------
        ch1 : str
        ch2 : str
            A, R, G or B
        """
        return "CHANCOPY_{}TO{}".format(ch1.upper(), ch2.upper())

    def __or__(self, other: 'Mix') -> str:
        if self.value == 'ALPHA' or other.value == 'ALPHA':
            return ''.join((self.value, other.value))
        raise TypeError("can combine only with 'ALPHA'")

    def __str__(self) -> str:
        return self.value  # type:ignore


class Color(ReapyObject):
    """More flexible way to make a color.

    Note
    ----
    Can be initialized as with separate args as well as with packed int:
        0xAARRGGBB

    Attributes
    ----------
    a : int
    r : int
    g : int
    b : int
    """

    a: int
    r: int
    g: int
    b: int

    def __init__(
        self,
        a: ty.Optional[int] = None,
        r: ty.Optional[int] = None,
        g: ty.Optional[int] = None,
        b: ty.Optional[int] = None
    ) -> None:
        if r == g == b is None:
            if a is None:
                raise TypeError('at least first int arg has to be specified')
            self.a = a >> 24 & 0xff
            self.r = a >> 16 & 0xff
            self.g = a >> 8 & 0xff
            self.b = a & 0xff
            return
        self.a = 0 if a is None else a
        self.r = 0 if r is None else r
        self.g = 0 if g is None else g
        self.b = 0 if b is None else b

    @property
    def _args(self) -> ty.Tuple[int, int, int, int]:
        return (self.a, self.r, self.g, self.b)

    def __int__(self) -> int:
        return (self.a << 24) + (self.r << 16) + (self.g << 8) + self.b

    def __repr__(self) -> str:
        return "Color(a={}, r={}, g={}, b={})".format(
            self.a, self.r, self.g, self.b
        )


class _BlitArea(ReapyObject):
    """Helper class for fixed-corners blit operations."""

    def __init__(
        self,
        dd: Dimentions,
        sd: Dimentions,
        scaled: bool = True,
        crop_source: bool = False
    ) -> None:
        (self.dd, self.sd, self.scaled) = (dd, sd, scaled)

    @property
    def _args(self) -> ty.Tuple[Dimentions, Dimentions, bool]:
        return self.dd, self.sd, self.scaled


class FixedCorners(ReapyObject):
    """Represents unscaled area of Bitmap."""

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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, tuple):
            return self.t == other
        if not isinstance(other, FixedCorners):
            return False
        return self.t == other.t

    def get_areas(self, dd: Dimentions,
                  sd: Dimentions) -> ty.Iterable[_BlitArea]:
        """Get all possible blit areas from the given dimentions.

        Parameters
        ----------
        dd : Dimentions
            destination dimentions
        sd : Dimentions
            source dimentions

        Returns
        -------
        Iterable[_BlitArea]
            List of all areas to blit.
        """
        areas: ty.List[_BlitArea] = []
        sl, st, sr, sb = self.left, self.top, self.right, self.bottom

        lw = max(min(dd.width, sl - sd.x), 0)  # max width of left
        th = max(min(dd.height, st - sd.y), 0)  # max height of top
        rw = max(min(dd.width - lw, sr), 0)  # max width of right
        bh = max(min(dd.height - th, sb), 0)  # max height of bottom

        # if needs resize
        if (dd.width, dd.height) < (rw + lw, th + bh):
            areas.append(_BlitArea(dd, sd, False))
            return areas

        # inner square
        areas.append(
            _BlitArea(
                Dimentions(
                    dd.x + lw, dd.y + th, dd.width - rw - lw,
                    dd.height - th - bh
                ),
                Dimentions(
                    sd.x + lw, sd.y + th, sd.width - rw - lw,
                    sd.height - th - bh
                )
            )
        )

        if (lw, th) != (0, 0):  # upper-left corner
            if sl > sd.x and st > sd.y:
                areas.append(
                    _BlitArea(
                        Dimentions(dd.x, dd.y, lw, th),
                        Dimentions(sd.x, sd.y, lw, th), False
                    )
                )
        if (rw, bh) != (0, 0):  # bottom-right corner
            if (dd.width, dd.height) > (lw, th):
                areas.append(
                    _BlitArea(
                        Dimentions(
                            dd.x + dd.width - rw, dd.y + dd.height - bh, rw, bh
                        ),
                        Dimentions(
                            sd.x + sd.width - rw, sd.y + sd.height - bh, rw, bh
                        ), False
                    )
                )
        if (th, rw) != (0, 0):  # upper-right corner
            if (dd.width, st) > (lw, sd.y):
                areas.append(
                    _BlitArea(
                        Dimentions(dd.x + dd.width - rw, dd.y, rw, th),
                        Dimentions(sd.x + sd.width - rw, sd.y, rw, th), False
                    )
                )
        if (lw, bh) != (0, 0):  # bottom-left corner
            if (sl, dd.height) > (sd.x, th):
                areas.append(
                    _BlitArea(
                        Dimentions(dd.x, dd.y + dd.height - bh, lw, bh),
                        Dimentions(sd.x, sd.y + sd.height - bh, lw, bh), False
                    )
                )
        if lw != 0:  # left strip
            if dd.height > th + bh:
                areas.append(
                    _BlitArea(
                        Dimentions(dd.x, dd.y + th, lw, dd.height - th - bh),
                        Dimentions(sd.x, sd.y + th, lw, sd.height - th - bh)
                    )
                )
        if rw != 0:  # right strip
            if dd.height > th + bh:
                areas.append(
                    _BlitArea(
                        Dimentions(
                            dd.x + dd.width - rw, dd.y + th, rw,
                            dd.height - th - bh
                        ),
                        Dimentions(
                            sd.x + sd.width - rw, sd.y + th, rw,
                            sd.height - th - bh
                        )
                    )
                )
        if th != 0:  # top strip
            if dd.width > lw + rw:
                areas.append(
                    _BlitArea(
                        Dimentions(dd.x + lw, dd.y, dd.width - lw - rw, th),
                        Dimentions(sd.x + lw, sd.y, sd.width - lw - rw, th)
                    )
                )
        if bh != 0:  # bottom strip
            if dd.width > lw + rw:
                areas.append(
                    _BlitArea(
                        Dimentions(
                            dd.x + lw, dd.y + dd.height - bh,
                            dd.width - lw - rw, bh
                        ),
                        Dimentions(
                            sd.x + lw, sd.y + sd.height - bh,
                            sd.width - lw - rw, bh
                        )
                    )
                )
        return areas


class Bitmap(ReapyObject):
    """Generalized LICE Bitmap.

    Note
    ----
    place Bitmap().cleanup() at atexit

    Attributes
    ----------
    fixed_corners : FixedCorners
        Can be set to prevent scaling of bitmap sides during `blit_scaled()`,
        doesn't work now for `blit_rotated()`
    ptr : JS.VoidPtr
        Bitmap handle.
    """

    def __init__(
        self,
        size: ty.Optional[ty.Tuple[int, int]] = None,
        ptr: ty.Optional[JS.VoidPtr] = None,
        fixed_corners: FixedCorners = FixedCorners(0, 0, 0, 0),
    ) -> None:
        size = (100, 100) if size is None else size
        self.ptr = JS.LICE_CreateBitmap(True, *size) if ptr is None else ptr
        self.fixed_corners = fixed_corners

    @property
    def _args(
        self
    ) -> ty.Tuple[ty.Optional[ty.Tuple[int, int]], ty.Optional[JS.VoidPtr],
                  FixedCorners]:
        return self.size, self.ptr, self.fixed_corners

    @property
    def size(self) -> ty.Tuple[int, int]:  # type:ignore
        with reapy.inside_reaper():
            return self.width, self.height

    @size.setter
    def size(self, size: ty.Tuple[int, int]) -> None:
        JS.LICE_Resize(self.ptr, *size)

    @property
    def width(self) -> int:
        return JS.LICE_GetWidth(self.ptr)

    @property
    def height(self) -> int:
        return JS.LICE_GetHeight(self.ptr)

    def cleanup(self) -> None:
        """Place it at atexit."""
        JS.LICE_DestroyBitmap(self.ptr)

    def blit(
        self,
        point: Point,
        bitmap: 'Bitmap',
        source_dim: Dimentions,
        alpha: float = 1.0,
        mode: ty.Union[str, Mix, MixBlit] = 'COPY'
    ) -> None:
        """Blit bitmap to self.

        Parameters
        ----------
        point : Point
            point on self to start blit on
        bitmap : Bitmap
        source_dim : Dimentions
            if less than bitmap size — will be cropped
        alpha : float, optional
            default to 1.0
        mode : Union[str, Mix, MixBlit], optional
            default to 'COPY'
        """
        JS.LICE_Blit(
            self.ptr,
            *point.t,
            bitmap.ptr,
            *source_dim.t,
            alpha,
            str(mode),
            encoding='ascii'
        )

    def _blit_area(
        self,
        area: _BlitArea,
        bitmap: 'Bitmap',
        alpha: float = 1.0,
        mode: ty.Union[str, Mix, MixBlit] = 'COPY'
    ) -> None:
        if area.scaled:
            JS.LICE_ScaledBlit(
                self.ptr,
                *area.dd.t,
                bitmap.ptr,
                *area.sd.t,
                alpha,
                str(mode),
                encoding='ascii'
            )
        else:
            self.blit(
                Point(area.dd.x, area.dd.y), bitmap, area.sd, alpha, mode
            )

    def blit_scaled(
        self,
        dest_dim: Dimentions,
        bitmap: 'Bitmap',
        source_dim: Dimentions,
        alpha: float = 1.0,
        mode: ty.Union[str, Mix, MixBlit] = 'COPY'
    ) -> None:
        """Blit bitmap to self, scaling it to given dimentions.

        Note
        ----
        If fixed_corners are not set to zero — bitmap will be scaled,
        saving scale of these areas. If source_dim x or y are positive —
        offset will be added to the saved area too.

        Parameters
        ----------
        dest_dim : Dimentions
            self area to scale bitmap to
        bitmap : Bitmap
        source_dim : Dimentions
            if less that bitmap size — will be cropped
            if more — will be stretched in
        alpha : float, optional
            default to 1.0
        mode : Union[str, Mix, MixBlit], optional
            default to 'COPY'
        """
        if bitmap.fixed_corners != (0, 0, 0, 0):
            fc = bitmap.fixed_corners
            dd = dest_dim
            sd = source_dim
            areas = fc.get_areas(dd, sd)
            self.map(
                '_blit_area', {'area': areas},
                defaults={
                    'bitmap': bitmap,
                    'alpha': alpha,
                    'mode': mode
                }
            )
            return
        JS.LICE_ScaledBlit(
            self.ptr,
            *dest_dim.t,
            bitmap.ptr,
            *source_dim.t,
            alpha,
            str(mode),
            encoding='ascii'
        )

    def blit_rotated(
        self,
        dest_dim: Dimentions,
        bitmap: 'Bitmap',
        source_dim: Dimentions,
        alpha: float = 1.0,
        mode: ty.Union[str, Mix, MixBlit] = 'COPY',
        angle: float = 0,
        center_adjust: ty.Tuple[float, float] = (0, 0),
        clip_to_source_rect: bool = True
    ) -> None:
        """Blit bitmap to self, rotate and scale.

        Parameters
        ----------
        dest_dim : Dimentions
            destination size and self position to scale on
        bitmap : Bitmap
        source_dim : Dimentions
            if less than bitmap size — it will be cropped
        alpha : float, optional
            default to 1.0
        mode : Union[str, Mix, MixBlit], optional
            default to "COPY"
        angle : float, optional
            rotation angle in radians (e.g. PI is 180°)
        center_adjust : Tuple[float, float], optional
            defaults to (0,0) (<x>, <y>)
            very ambiguos parameter that needs to be investigated.
            As I understand it: positive values move center in negative
            direction, and moving amount depends on source_dim.
        clip_to_source_rect : bool, optional
            To not being clipped source_dim has to be larger than bitmap size
        """
        JS.LICE_RotatedBlit(
            self.ptr,
            *dest_dim.t,
            bitmap.ptr,
            *source_dim.t,
            angle,
            *center_adjust,
            clip_to_source_rect,
            alpha,
            str(mode),
            encoding='ascii'
        )


class Canvas(Bitmap):
    """Drawable LICE bitmap within optional background.

    Attributes
    ----------
    alpha : float
    bg_color : Union[int, Color]
        0xAARRGGBB
    color : Union[int, Color]
        Foreground color
    mode : Union[str, Mix]
        Drawing mix mode
    """

    def __init__(
        self,
        size: ty.Optional[ty.Tuple[int, int]] = None,
        ptr: ty.Optional[JS.VoidPtr] = None,
        fixed_corners: FixedCorners = FixedCorners(0, 0, 0, 0),
        bg_color: ty.Union[int, Color] = 0xff000000,
        color: ty.Union[int, Color] = 0xffffffff,
        alpha: float = 1,
        mode: ty.Union[str, Mix] = 'COPY'
    ) -> None:
        super().__init__(size, ptr, fixed_corners)
        self.bg_color = bg_color
        self.color = color
        self.alpha = alpha
        self.mode = mode
        setattr(self, 'draw', self._draw_wrap(self.draw))

    @property
    def _args(self) -> ty.Tuple[ty.Any, ...]:  # type:ignore
        return (
            *super()._args, self.bg_color, self.color, self.alpha, self.mode
        )

    def _draw_wrap(self, draw: ty.Callable[[], None]) -> ty.Callable[[], None]:
        """Internal wrapper of user draw."""

        def wrapper() -> None:
            with reapy.inside_reaper():
                JS.LICE_Clear(self.ptr, int(self.bg_color))
                try:
                    draw()
                except Exception as e:
                    print(e)
                    raise e

        return wrapper

    def draw(self) -> None:
        """Here art happens!

        Note
        ----
        Has to be binded to events manually.
        """

    def rect_fill(
        self,
        dimentions: Dimentions,
        color: ty.Optional[ty.Union[int, Color]] = None,
        alpha: ty.Optional[float] = None,
        mode: ty.Optional[ty.Union[str, Mix]] = None
    ) -> None:
        JS.LICE_FillRect(
            self.ptr,
            *dimentions.t,
            int(color if color is not None else self.color),
            alpha if alpha is not None else self.alpha,
            str(mode if mode is not None else self.mode),
        )

    def rect_round(
        self,
        dimentions: Dimentions,
        color: ty.Optional[ty.Union[int, Color]] = None,
        alpha: ty.Optional[float] = None,
        mode: ty.Optional[ty.Union[str, Mix]] = None,
        cornerradius: int = 5,
        antialias: bool = True,
        fill: bool = True,
    ) -> None:
        JS.LICE_RoundRect(
            self.ptr,
            *dimentions.t,
            cornerradius=cornerradius,
            color=int(color if color is not None else self.color),
            alpha=alpha if alpha is not None else self.alpha,
            mode=str(mode if mode is not None else self.mode),
            antialias=antialias,
        )


class PNG(Canvas):
    """LICE png handler."""

    def __init__(
        self,
        size: ty.Optional[ty.Tuple[int, int]] = None,
        ptr: ty.Optional[JS.VoidPtr] = None,
        fixed_corners: FixedCorners = FixedCorners(0, 0, 0, 0),
        bg_color: ty.Union[int, Color] = 0xff000000,
        color: ty.Union[int, Color] = 0xffffffff,
        alpha: float = 1,
        mode: ty.Union[str, Mix] = 'COPY',
        filename: ty.Optional[str] = None,
        encoding: str = 'utf-8'
    ) -> None:
        if ptr == filename is None:
            raise TypeError("Either ptr or filename have to be specified")
        if ptr is not None:
            return super().__init__(size, ptr, fixed_corners)
        ptr = self._load(ty.cast(str, filename), encoding)
        super().__init__(
            size, ptr, fixed_corners, bg_color, color, alpha, mode
        )

    def _load(self, filename: str, encoding: str) -> JS.VoidPtr:
        fallback = 'ascii'

        for i in range(20):
            if i >= 15:
                encoding = fallback
            ptr = JS.LICE_LoadPNGEx(filename, encoding)
            print(
                'loaded from "{}" with encoding "{}". Returned: {}'.format(
                    filename, encoding, ptr
                )
            )
            if int(ptr) != 0:
                return ptr
        raise ResourceLoadError(
            "can't load PNG from file {} with encoding {}".format(
                filename, encoding
            )
        )


class CompositedWindow:
    """Helper class for efficient bitmap placing over the window.

    Usage
    -----
    * initialize within window handle or pointer
    * use composite() when bitmap has to be placed, moved or has been updated
    * call invalidate on every event loop iteration
    * call refresh on invasive procedures like window resize
    * composite all bitmaps again after refresh
    """

    def __init__(self, window: Window) -> None:
        self.__ptr = window.ptr
        self._bitmaps: ty.Dict[JS.VoidPtr, Coordinates] = {}
        self._invalidate_rect: ty.Optional[Coordinates] = None
        self._wind_coords: ty.Optional[Coordinates] = None

    @property
    def bitmaps(self) -> ty.Dict[JS.VoidPtr, Coordinates]:
        """All bitmaps being composited right now.

        :type: ty.Dict[JS.VoidPtr, Coordinates]
        """
        return self._bitmaps

    def composite(
        self, bitmap: 'Bitmap', wind_dimentions: Dimentions,
        bitm_dimentions: Dimentions
    ) -> None:
        """Place bitmap over the window.

        Parameters
        ----------
        bitmap : JS.VoidPtr
        wind_dimentions : Dimentions
            * if width or height are -1 bitmap will be stretched
            * if width or height are different, bitmap will be stretched
        bitm_dimentions : Dimentions
            if width or height are different bitmap will be cropped
        """
        bitmap_p = bitmap.ptr
        wd = wind_dimentions
        bd = bitm_dimentions
        JS.Composite(self.__ptr, *wd.t, bitmap_p, *bd.t)

        wr = self._window_coordinates()
        new = Coordinates(
            left=(bd.x + wd.x) if wd.width != -1 else 0,
            right=(bd.x + bd.width + wd.x) if wd.width != -1 else wr.right,
            top=(bd.y + wd.y) if wd.height != -1 else 0,
            bottom=(bd.y + bd.height + wd.y) if wd.width != -1 else wr.bottom
        )
        new_max = new
        if bitmap_p in self._bitmaps:
            new_max = new.max(self._bitmaps[bitmap_p])
        self._bitmaps[bitmap_p] = new
        if self._invalidate_rect is None:
            self._invalidate_rect = new_max
        else:
            self._invalidate_rect = self._invalidate_rect.max(new_max)

    def _window_coordinates(self) -> Coordinates:
        if self._wind_coords is None:
            ret, l, t, r, b = JS.Window_GetRect(self.__ptr)
            if b - t < 0:
                t, b = b, t
            self._wind_coords = Coordinates(0, 0, r - l, b - t)
        return self._wind_coords

    def invalidate(self, erase_bg: bool = True) -> None:
        """Update changed window area or do nothing.

        Parameters
        ----------
        erase_bg : bool, optional
            Actually, it has to be investigated.
        """
        if self._invalidate_rect is None:
            return
        JS.Window_InvalidateRect(
            self.__ptr, *self._invalidate_rect.t, erase_bg
        )
        self._invalidate_rect = None

    def refresh(self) -> None:
        """Erase all bindings to bitmaps and refresh invalidated area."""
        self._invalidate_rect = None
        self._wind_coords = None
        self._bitmaps = {}
