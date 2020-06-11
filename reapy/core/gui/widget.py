import typing as ty

import reapy
from . import JS
from reapy.errors import ResourceLoadError
from .misc import Dimentions, Coordinates, Point, Size, mouse_pos
from .swell_translations import WS
from . import events as ev
from .window import Window
from . import lice
from . import swell_translations as sw_t
from .singleton import UUID, Singleton

EVENT_HANDLER = ev.EventHandler()


class EvResize(ev.Event):
    """Indicates Widget resize."""

    def __init__(self, size: Size) -> None:
        self.size = size

    def _args(self) -> ty.Tuple[Size]:
        return (self.size, )


class EvWindowMessage(ev.Event):
    """Fired when general WindowMessage is intercepted.

    Note
    ----
    Not fired if specific WM intercepted.
    """

    def __init__(
        self,
        msg: str,
        passedthrough: bool,
        time: float,
        wParamLow: int,
        wParamHigh: int,
        lParamLow: int,
        lParamHigh: int,
    ) -> None:
        self.msg = msg
        self.passedthrough = passedthrough
        self.time = time
        self.wParamLow = wParamLow
        self.wParamHigh = wParamHigh
        self.lParamLow = lParamLow
        self.lParamHigh = lParamHigh

    @property
    def _args(self) -> ty.Tuple[str, bool, float, int, int, int, int]:
        return (
            self.msg, self.passedthrough, self.time, self.wParamLow,
            self.wParamHigh, self.lParamLow, self.lParamHigh
        )

    def __repr__(self) -> str:
        return (
            "WM(msg={}, passedthrough={}, time={}, wParamLow={},"
            " wParamHigh={}, lParamLow={}, lParamHigh={},"
        ).format(
            self.msg, self.passedthrough, self.time, self.wParamLow,
            self.wParamHigh, self.lParamLow, self.lParamHigh
        )


class EvKeyDownChar(ev.Event):
    """Fired when non-system key is pressed.

    Attributes
    ----------
    time: float
    char: str
        key unicode representation
    mod: vVirtKey
        flags of ctrl|alt|shift buttons held
    """

    def __init__(self, time: float, char: str, mod: sw_t.vVirtKey) -> None:
        self.time, self.char, self.mod = time, char, sw_t.vVirtKey(mod)

    @property
    def _args(self) -> ty.Tuple[float, str, sw_t.vVirtKey]:
        return self.time, self.char, self.mod


class EvKeyDownSys(ev.Event):
    """Fired when system key is pressed.

    Attributes
    ----------
    time:float
    key: vKey
    mod: vVirtKey
        flags of ctrl|alt|shift buttons held
    """

    def __init__(
        self, time: float, key: sw_t.vKey, mod: sw_t.vVirtKey
    ) -> None:
        self.time, self.key, self.mod = (
            time, sw_t.vKey(key), sw_t.vVirtKey(mod)
        )

    @property
    def _args(self) -> ty.Tuple[float, sw_t.vKey, sw_t.vVirtKey]:
        return self.time, self.key, self.mod


class WM_Handler:
    """Intercepts and handles WindowMessages.

    Attributes
    ----------
    hwnd : VoidPtr
        widget hwnds
    message_times : Dict[str, float]
        last time message was recieved
    widget : Widget
    """

    hwnd: JS.VoidPtr

    def __init__(
        self, hwnd: JS.VoidPtr, event_handler: ev.EventHandler,
        widget_uuid: UUID
    ) -> None:
        self.hwnd, self.event_handler, self.widget_uuid = (
            hwnd, event_handler, widget_uuid
        )
        self.message_names: ty.List[str] = [
            "WM_CAPTURECHANGED",
            "WM_LBUTTONDOWN",
            "WM_LBUTTONUP",
            "WM_LBUTTONDBLCLK",
            "WM_NCLBUTTONDOWN",
            "WM_CHAR",
            "WM_KEYDOWN",
            "WM_SYSKEYDOWN",
            "WM_ACTIVATE",
            "WM_MOUSELEAVE",
            "WM_MOUSEACTIVATE",
        ]
        self.message_times = {msg: 0.0 for msg in self.message_names}

    def fire(self, event: ev.Event) -> None:
        """Shortcut to widget.fire_event()."""
        self.event_handler.fire_event(event, [self.widget_uuid])

    def setup(self) -> None:
        """Start intercepting messages."""
        for msg in self.message_names:
            ret = JS.WindowMessage_Intercept(self.hwnd, msg, False)
            print("%s, intercept ret: %s" % (msg, ret))

    def run(self) -> None:
        """Main fmethod, runs every frame."""
        hwnd = self.hwnd
        mess_times = self.message_times

        for msg, l_time in mess_times.items():
            (
                pOk, passedthrough, n_time, wParamLow, wParamHigh, lParamLow,
                lParamHigh
            ) = JS.WindowMessage_Peek(hwnd, msg)
            if n_time > l_time:
                mess_times[msg] = n_time
                msg_l = msg.lower()
                wm = EvWindowMessage(
                    msg, passedthrough, n_time, wParamLow, wParamHigh,
                    lParamLow, lParamHigh
                )
                if hasattr(self, "on_%s" % msg_l):
                    return getattr(self, "on_%s" % msg_l)(  # type:ignore
                        wm
                    )

                return self.on_wm(wm)

    def on_wm(self, wm: EvWindowMessage) -> None:
        """Generic handler that just pushes message to widget."""
        self.fire(wm)

    def on_wm_keydown(self, wm: EvWindowMessage) -> None:
        char = chr(wm.wParamLow)
        mod = sw_t.vVirtKey(wm.lParamLow)

        # if fired as vKey (true for latin layout)
        if 0b1 & wm.lParamLow:
            if wm.wParamLow in sw_t.vKey.__members__.values():
                self.on_wm_syskeydown(wm)
                if wm.wParamLow not in sw_t.vNumKey.__members__.values():
                    return
                else:
                    char = sw_t.vNumKey(wm.wParamLow).char()

            # handling upper-lover case
            if mod & sw_t.vVirtKey.SHIFT:
                char = char.upper()
            else:
                char = char.lower()
        self.fire(EvKeyDownChar(wm.time, char, mod))

    def on_wm_syskeydown(self, wm: EvWindowMessage) -> None:
        if wm.wParamLow not in sw_t.vKey.__members__.values():
            # should exception be raised?
            print('can not decode message: %s' % wm)
            return
        self.fire(
            EvKeyDownSys(
                wm.time, sw_t.vKey(wm.wParamLow), sw_t.vVirtKey(wm.lParamLow)
            )
        )

    def cleanup(self) -> None:
        """End intercepting messages."""
        JS.WindowMessage_Release(
            self.hwnd, ','.join(tuple(self.message_names))
        )


class Layout(Singleton):

    def __init__(
        self,
        default_rule: object,
        window: ty.Optional['Window'] = None
    ) -> None:
        self.default_rule = default_rule
        self.rules: ty.Dict[Widget, object] = {}
        self.window = window

    @property
    def _args(self) -> ty.Tuple[ty.Optional['Window'], object]:
        return (self.window, self.default_rule)

    @property
    def _state(self) -> ty.Dict[str, object]:
        return {**super()._state, "rules": self.rules}

    def add_child(
        self, child: 'Widget', rule: ty.Optional[object] = None
    ) -> None:
        if rule is None:
            rule = self.default_rule
        self.rules[child] = rule

    def delete_child(self, child: 'Widget') -> None:
        del self.rules[child]

    def __getitem__(self, key: 'Widget') -> object:
        return self.rules[key]

    def __setitem__(self, key: 'Widget', rule: object) -> None:
        self.rules[key] = rule

    def do(self) -> None:
        """Pllace widgets windows over the window."""
        for child, rule in self.rules.items():
            child.position = rule  # type:ignore


class Widget(ev.EventClient):
    """The very root element of GUI."""

    def __init__(
        self,
        size: Size = Size(100, 100),
        position: Point = Point(0, 0),
        window_title: str = "Widget",
        bg_color: ty.Union[int, lice.Color] = 0xff000000,
        window: ty.Optional[Window] = None,
        layout: ty.Optional[Layout] = None,
    ) -> None:
        super().__init__(EVENT_HANDLER)
        print('init with args:', size, position, window_title, bg_color)
        self._window = Window(
            dimentions=Dimentions(*position.t, *size.t),
            title=window_title,
            class_name='ReapyWindow'
        ) if window is None else window
        print(f'window: {self._window}, position: {self.window.position}')

        self.canvas = lice.Canvas(
            size=size,
            ptr=None,
            fixed_corners=lice.FixedCorners(0, 0, 0, 0),
            bg_color=bg_color
        )
        print(f'canvas: {self.canvas}')
        self.composer = lice.CompositedWindow(self._window)
        self.wm_handler: ty.Optional[WM_Handler] = None
        self.z_order: float = 0
        self._layout = Layout(Point(0, 0)) if layout is None else layout
        self._layout.window = self.window

    @property
    def _kwargs(self) -> ty.Dict[str, object]:
        return {
            **super()._kwargs,
            "window": self.window,
            "layout": self._layout,
        }

    @property
    def _state(self) -> ty.Dict[str, object]:
        return {
            **super()._state,
            "parent_window": self.parent,
            # "window": self.window,
            "wm_handler": self.wm_handler,
            "composer": self.composer,
            "z_order": self.z_order,
            # "_layout": self._layout,
        }

    def __hash__(self) -> int:
        return hash(self.uuid)

    @property
    def layout(self) -> Layout:
        return self._layout

    @layout.setter
    def layout(self, layout: Layout) -> None:
        self._layout = layout
        self._layout.window = self.window

    @property
    def window(self) -> Window:
        return self._window

    @window.setter
    def window(self, window: Window) -> None:
        if window == self._window:
            return
        JS.Window_Destroy(self._window.ptr)
        self._window = window

    @property
    def dimentions(self) -> Dimentions:
        return self.window.dimentions

    @dimentions.setter
    def dimentions(self, dimentions: Dimentions) -> None:
        self.window.dimentions = dimentions

    @property
    def coordinates(self) -> Coordinates:
        return self.window.coordinates

    @coordinates.setter
    def coordinates(self, coordinates: Coordinates) -> None:
        self.window.coordinates = coordinates

    @property
    def position(self) -> Point:
        return self.window.position

    @position.setter
    def position(self, pos: Point) -> None:
        self.window.position = pos

    @property
    def size(self) -> Size:
        return self.window.size

    @size.setter
    def size(self, size: Size) -> None:
        self.window.size = size
        self.canvas.size = size
        self.canvas.draw()
        # self._handle_z_order()

    def add_child(self, child: ev.EventClient) -> None:
        print('add_child')
        super().add_child(child)
        if isinstance(child, Widget):
            child.window.parent = self.window
            self._layout.add_child(child)
            if self.is_running():
                self._layout.do()

    def _handle_focus(self) -> None:
        # I should remember what flags indicate but... not.
        mouse_flags = JS.Mouse_GetState(0b10000011)
        if mouse_flags != 0:
            mx, my = mouse_pos()
            sl, st, sr, sb = self.coordinates
            if sl <= mx <= sr and st <= my <= sb:
                # self._focused = True
                self.window.focus()
            # elif self._focused:
            #     self._focused = False
            #     JS.Window_SetFocus(JS.Window_FromPoint(mx, my))

    def _handle_z_order(self) -> None:
        z_layers: ty.Dict[float, ty.List[Window]] = {}
        for child in self.childs.values():
            if not isinstance(child, Widget):
                continue
            z = child.z_order
            if z not in z_layers:
                z_layers[z] = []
            z_layers[z].append(child.window)
        for _, wnds in sorted(z_layers.items()):
            for wnd in wnds:
                wnd.bring_to_front()

    def setup(self) -> None:
        self.wm_handler = WM_Handler(
            self.window.ptr, self.event_handler, self.uuid
        )
        print(
            f'setup of {self}', f'wm_handler: {self.wm_handler}',
            f'window: {self.window.title}', f'position: {self.position}'
        )
        self.window.bring_to_front()
        self.wm_handler.setup()
        self.canvas.draw()
        self.composer.composite(
            self.canvas, Dimentions(0, 0, *self.window.size),
            Dimentions(0, 0, *self.canvas.size)
        )
        self.window.update()
        # self._handle_z_order()
        self._layout.do()

    def _loop_frame(self) -> None:
        if self.wm_handler is not None:
            self.wm_handler.run()
        self.composer.invalidate()
        # self._handle_focus()
        if self.size != self.canvas.size:
            self.size = self.size
            self.fire_event(EvResize(self.size), clients=ev.EventTarget.self_)
        for child in self.childs.values():
            child._loop_frame()

    def cleanup(self) -> None:
        super().cleanup()
        if self.wm_handler is not None:
            self.wm_handler.cleanup()
        self.canvas.cleanup()
        self.window.cleanup()

    def on_event(self, event: ev.Event) -> None:
        if isinstance(event, EvResize):
            return self.on_resize(event.size)
        if isinstance(event, EvWindowMessage):
            print(f'{self.window.title}:', event)
        return super().on_event(event)

    def on_resize(self, size: Size) -> None:
        """Called when size changed."""
        self._layout.do()
        self.canvas.draw()
        self.composer.refresh()
        self.composer.composite(
            self.canvas, Dimentions(0, 0, *self.window.size),
            Dimentions(0, 0, *self.canvas.size)
        )
