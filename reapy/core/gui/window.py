import typing as ty
import os
from time import sleep
import atexit
import platform
from uuid import uuid4

import reapy
from . import JS_API as JS
from . import swell_translations as sw_t
from .singleton import Singleton
from .events import EventHandler, EventClient, Event
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.errors import ResourceLoadError

GUI_SECTION = "reapy_gui"

_lua_template = """
gfx.init("{name}", {width}, {height}, {dockstate}, {x}, {y})
function main()
    ext_dock = reaper.GetExtState("{ext_sect}", "{name}_dockstate")
    if ext_dock ~= "" then
        gfx.dock(tonumber(ext_dock))
        reaper.SetExtState("{ext_sect}", "{name}_dockstate", "", false)
    end
    gfx.update()
    reaper.SetExtState("{ext_sect}", "{name}_dock_out",
        tostring(gfx.dock(-1)), false)
    local char = gfx.getchar()
    if reaper.GetExtState("{ext_sect}", "{name}") ~= "close" and
    char ~= 27 and char ~= -1
    then
        reaper.defer(main)
    else
        reaper.SetExtState("{ext_sect}", "{name}", "", false)
    end
end
main()
"""


class EvWindowMessage(Event):

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


class EvKeyDownChar(Event):

    def __init__(self, time: float, char: str, mod: sw_t.vVirtKey) -> None:
        self.time, self.char, self.mod = time, char, sw_t.vVirtKey(mod)

    @property
    def _args(self) -> ty.Tuple[float, str, sw_t.vVirtKey]:
        return self.time, self.char, self.mod


class EvKeyDownSys(Event):

    def __init__(
        self, time: float, key: sw_t.vKey, mod: sw_t.vVirtKey
    ) -> None:
        self.time, self.key, self.mod = (
            time, sw_t.vKey(key), sw_t.vVirtKey(mod)
        )

    @property
    def _args(self) -> ty.Tuple[float, sw_t.vKey, sw_t.vVirtKey]:
        return self.time, self.key, self.mod


class EvFrame(Event):
    """Fired every loop frame."""


class EvStart(Event):
    """Fired on mainloop start."""


class EvExit(Event):
    """Fired on mainloop exit."""


class EvResized(Event):
    """Fired on window resizing."""

    def __init__(self, new_size: ty.Tuple[int, int]) -> None:
        self.width, self.height = new_size
        self.size = new_size


class WM_Handler:
    hwnd: JS.VoidPtr

    def __init__(self, toplevel: 'TopLevel') -> None:
        self.toplevel = toplevel
        # self._event_handler = toplevel.event_handler
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

    def fire(self, event: Event) -> None:
        self.toplevel.fire_event(event)

    def start(self) -> None:
        for msg in self.message_names:
            self.hwnd = self.toplevel.hwnd
            ret = JS.WindowMessage_Intercept(self.hwnd, msg, False)
            print("%s, intercept ret: %s" % (msg, ret))

    def run(self) -> None:
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
        self.fire(wm)

    def on_wm_keydown(self, wm: EvWindowMessage) -> None:
        char = chr(wm.wParamLow)
        mod = sw_t.vVirtKey(wm.lParamLow)
        if 0b1 & wm.lParamLow:
            if wm.wParamLow in sw_t.vKey.__members__.values():
                self.on_wm_syskeydown(wm)
                if wm.wParamLow not in sw_t.vNumKey.__members__.values():
                    return
                else:
                    char = sw_t.vNumKey(wm.wParamLow).char()
            if mod & sw_t.vVirtKey.SHIFT:
                char = char.upper()
            else:
                char = char.lower()
        self.fire(EvKeyDownChar(wm.time, char, mod))
        # self.toplevel.on_key_char(wm.time, char, mod)

    def on_wm_syskeydown(self, wm: EvWindowMessage) -> None:
        if not wm.wParamLow in sw_t.vKey.__members__.values():
            print('can not decode message: %s' % wm)
            return
        self.fire(
            EvKeyDownSys(
                wm.time, sw_t.vKey(wm.wParamLow), sw_t.vVirtKey(wm.lParamLow)
            )
        )
        # self.toplevel.on_key_sys(
        #     wm.time, sw_t.vKey(wm.wParamLow), sw_t.vVirtKey(wm.lParamLow)
        # )

    def cleanup(self) -> None:
        JS.WindowMessage_Release(
            self.hwnd, ','.join(tuple(self.message_names))
        )


def mouse_pos() -> ty.Tuple[int, int]:
    return RPR.GetMousePosition(0, 0)  # type:ignore


class TopCanvas(EventClient):
    ptr: JS.VoidPtr

    def __init__(
        self,
        toplevel: 'TopLevel',
        size: ty.Optional[ty.Tuple[int, int]] = None
    ) -> None:
        self._size = size
        self.toplevel = toplevel
        super().__init__(self.toplevel.event_handler)

    @reapy.inside_reaper()  # type:ignore
    @property
    def size(self) -> ty.Tuple[int, int]:
        if self._size is None:
            rect = JS.Window_GetRect(RPR.GetMainHwnd())  # type:ignore
            l, t, r, b = JS.Window_GetViewportFromRect(*rect[1:], True)
            if platform.system() == 'Darwin':
                self._size = r - l, t - b
            else:
                self._size = r - l, b - t
        return self._size

    @property
    def _args(self) -> ty.Tuple['TopLevel', ty.Tuple[int, int]]:
        return self.toplevel, self.size

    def on_event(self, event: Event) -> None:
        if isinstance(event, EvStart):
            return self.setup()
        # if isinstance(event, EvFrame):
        #     return self.run()
        if isinstance(event, EvExit):
            return self.cleanup()

    def setup(self) -> None:
        self.ptr = JS.LICE_CreateBitmap(True, *self.size)
        sOk = JS.Composite(
            self.toplevel.hwnd, 0, 0, *self.size, self.ptr, 0, 0, *self.size
        )
        codes = {
            -1: 'windowHWND is not a window',
            -2: 'Could not obtain the original window process',
            -4: 'sysBitmap is not a LICE bitmap',
            -5: 'sysBitmap is not a system bitmap',
            -6: 'Could not obtain the window HDC'
        }
        if sOk != 1:
            raise ResourceLoadError(
                'canvas {} failed to Composite. {}:{}'.format(
                    self, sOk, codes[sOk]
                )
            )
        print(f'canvas made: {self.ptr, sOk, self.size}')

    def cleanup(self) -> None:
        print(f'destroing canvas {self.ptr}')
        JS.LICE_DestroyBitmap(self.ptr)


class TopLevel(EventClient):
    _wm_handler: WM_Handler

    # _object_index: ty.Dict[int, 'TopLevel'] = {}

    def __init__(
        self,
        name: str,
        x: int = 100,
        y: int = 100,
        width: int = 100,
        height: int = 100,
        dockstate: int = 1,
        autofocus: bool = True,
        canvas_size: ty.Optional[ty.Tuple[int, int]] = None
    ) -> None:
        super().__init__(EventHandler())
        self.name, self.x, self.y, self.width, self.height, self._dockstate = (
            name, x, y, width, height, dockstate
        )
        self.filename = "{}_gui.lua".format(name)
        self._hwnd: ty.Optional[JS.VoidPtr] = None

        if self._check_for_window() <= 0:
            self._running = False
        else:
            self._running = True
        self._focused = False
        self.autofocus = autofocus
        self._wm_handler = WM_Handler(self)
        self._last_size = (width, height)
        self.canvas = TopCanvas(self)

    @property
    def _args(
        self
    ) -> ty.Tuple[str, int, int, int, int, int, bool, ty.Tuple[int, int]]:
        return (
            self.name, self.x, self.y, self.width, self.height,
            self._dockstate, self.autofocus, self.canvas.size
        )

    @reapy.inside_reaper()  # type:ignore
    @property
    def hwnd(self) -> JS.VoidPtr:
        if self._hwnd is None:
            raise RuntimeError('Window is not initialized')
        return self._hwnd

    def _check_for_window(self) -> int:
        ret, array = JS.Window_ArrayFindEx(self.name, True)
        # print(f'ret = {ret}')
        if ret <= 0:
            return ret
        self._hwnd = JS.reaper_array_to_hwnd(array)[0]
        return ret

    @reapy.inside_reaper()
    def _launch(self) -> JS.VoidPtr:
        reapy.set_ext_state(GUI_SECTION, self.name, "")
        print(f'filename: {os.path.abspath(self.filename)}')
        with open(self.filename, 'w') as f:
            f.write(
                _lua_template.format(
                    name=self.name,
                    x=self.x,
                    y=self.y,
                    width=self.width,
                    height=self.height,
                    dockstate=self._dockstate,
                    ext_sect=GUI_SECTION
                )
            )
        action = reapy.add_reascript(self.filename)
        reapy.perform_action(action)

        # here self.hwnd become real. Not as verbose, as I would like.
        if self._check_for_window() <= 0:
            raise RuntimeError("can not find gui window")
        self.update_coords()

        self._wm_handler.start()
        return self.hwnd

    def update_coords(self) -> None:
        l, t, r, b = self.coordinates
        self.x, self.y, self.width, self.height = l, t, r - l, b - t
        if reapy.is_inside_reaper():
            if (r - l, b - t) < self._last_size:
                self._last_size = self.width, self.height
                self.fire_event(EvResized(self._last_size))
        else:
            self._update_coords_inside()

    @reapy.inside_reaper()
    def _update_coords_inside(self) -> None:
        self.update_coords()

    @reapy.inside_reaper()
    def _kill(self) -> None:
        print('exiting from _kill')
        self._running = False
        self._wm_handler.cleanup()
        self.fire_event(EvExit(), with_canvas=True)
        reapy.set_ext_state(GUI_SECTION, self.name, "close")
        reapy.remove_reascript(self.filename)
        os.remove(self.filename)

    @reapy.inside_reaper()
    def running(self) -> bool:
        return self._running

    def fire_event(self, event: Event, with_canvas: bool = False) -> None:
        clients: ty.List[EventClient] = [self]
        if with_canvas:
            clients.append(self.canvas)
        self.event_handler.fire_event(event, clients)

    def mainloop(self, blocking: bool = True) -> None:
        # self._event_handler.register_client(self)
        self.start(self.event_handler, self.canvas)
        if not reapy.is_inside_reaper():
            atexit.register(self._at_exit)
            # if not blocking:
            #     return
            while self.running():
                with reapy.inside_reaper():
                    self.event_handler.fire_queue()

    @reapy.inside_reaper()
    def _at_exit(self) -> None:
        self.cleanup()
        if not self.running():
            return
        self._kill()

    @reapy.inside_reaper()
    def start(self, ev_handler: EventHandler, canvas: TopCanvas) -> None:
        self._running = True
        self.event_handler = ev_handler
        self.canvas = canvas
        self._launch()
        reapy.at_exit(self._at_exit)
        self.fire_event(EvStart(), with_canvas=True)
        self._loop()

    @reapy.inside_reaper()
    def _loop(self) -> None:
        if not RPR.ValidatePtr(  # type:ignore
            self.hwnd, "HWND"
        ) and self._running:
            self._kill()
            return
        try:
            self.event_handler.fire_event(EvFrame(), [self])
            self._handle_focus()
            self._wm_handler.run()
            # self._handle_wm()
            reapy.defer(self._loop)
        except KeyboardInterrupt as e:
            self._kill()
            raise e

    @property
    def coordinates(self) -> ty.Tuple[int, int, int, int]:
        """Normalized window rectangle, e.g. top is always less than bottom.

        Returns
        -------
        ty.Tuple[int, int, int, int]
            left, top, right, bottom
        """
        _, sl, st, sr, sb = JS.Window_GetRect(self.hwnd)
        if platform.system() == 'Darwin':
            return sl, sb, sr, st
        return sl, st, sr, sb

    def _handle_focus(self) -> None:
        if not self.autofocus:
            return
        mouse_flags = JS.Mouse_GetState(0b10000011)
        if mouse_flags != 0:
            mx, my = mouse_pos()
            sl, st, sr, sb = self.coordinates
            if sl <= mx <= sr and st <= my <= sb:
                self._focused = True
                JS.Window_SetFocus(self.hwnd)
            elif self._focused:
                self._focused = False
                JS.Window_SetFocus(JS.Window_FromPoint(mx, my))

    def on_event(self, event: Event) -> None:
        if isinstance(event, EvFrame):
            self.update_coords()
            return self.run()
        if isinstance(event, EvKeyDownChar):
            # print('catched EvKeyDownChar')
            return self.on_key_char(event)
        if isinstance(event, EvKeyDownSys):
            return self.on_key_sys(event)

        # move all down
        if isinstance(event, EvStart):
            return self.setup()
        if isinstance(event, EvExit):
            return self.cleanup()

    def setup(self) -> None:
        """Called at first mainloop iteration."""

    def run(self) -> None:
        """Called every loop iteration."""

    def cleanup(self) -> None:
        """Called at exit."""

    @property
    def dock(self) -> int:
        """Raw reaper window dockstate.

        :type: int
            the basic rule: 0 — floating, 1 — docked
        """
        ret = reapy.get_ext_state(GUI_SECTION, "%s_dock_out" % self.name)
        self._dockstate = int(float(ret))
        return self._dockstate

    @dock.setter
    def dock(self, value: int) -> None:
        self._dockstate = value
        reapy.set_ext_state(
            GUI_SECTION, "%s_dockstate" % self.name, str(value), False
        )

    def on_key_char(self, event: EvKeyDownChar) -> None:
        print(
            'on_key_char(time={}, char={}, mod={})'.format(
                event.time, event.char, event.mod.__repr__()
            )
        )

    def on_key_sys(self, event: EvKeyDownSys) -> None:
        print(
            "on_key_sys(time={}, key={}, mod={})".format(
                event.time, repr(event.key), repr(event.mod)
            )
        )
