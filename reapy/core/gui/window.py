import typing as ty
import os
from time import sleep
import atexit

import reapy
from . import JS_API as JS
from reapy import reascript_api as RPR
from reapy.core import ReapyObject

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


class WM_Handler:

    def __init__(self) -> None:
        self.message_times: ty.Dict[str, float] = {
            "WM_LBUTTONDOWN": 0,
            "WM_LBUTTONUP": 0,
            "WM_LBUTTONDBLCLK": 0,
        }


class TopLevel(ReapyObject):

    def __init__(
        self,
        name: str,
        x: int = 100,
        y: int = 100,
        width: int = 100,
        height: int = 100,
        dockstate: int = 1
    ) -> None:
        self.name, self.x, self.y, self.width, self.height, self._dockstate = (
            name, x, y, width, height, dockstate
        )
        self.filename = "{}_gui.lua".format(name)
        self._hwnd: ty.Optional[JS.VoidPtr] = None
        self.wm_handler = WM_Handler()
        if self._check_for_window() <= 0:
            self._running = False
        else:
            self._running = True

    @property
    def _args(self) -> ty.Tuple[str, int, int, int, int, int]:
        return (
            self.name, self.x, self.y, self.width, self.height, self._dockstate
        )

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
        if self._check_for_window() <= 0:
            raise RuntimeError("can not find gui window")
        ret, l, t, r, b = JS.Window_GetRect(self.hwnd)
        if ret:
            self.x, self.y, self.width, self.height = l, t, r - l, b - t
        msgstr = ', '.join(tuple(self.wm_handler.message_times.keys()))
        print(self.hwnd)
        for msg in self.wm_handler.message_times.keys():
            ret = JS.WindowMessage_Intercept(self.hwnd, msg, False)
            print(f"{msg} intercept ret: {ret}")
        return self.hwnd

    @reapy.inside_reaper()
    def _kill(self) -> None:
        print('exiting from _kill')
        self._running = False
        JS.WindowMessage_Release(
            self.hwnd, ','.join(tuple(self.wm_handler.message_times.keys()))
        )
        reapy.set_ext_state(GUI_SECTION, self.name, "close")
        reapy.remove_reascript(self.filename)
        os.remove(self.filename)

    @reapy.inside_reaper()
    def running(self) -> bool:
        # print(f'running = {self._running}, inside: {reapy.is_inside_reaper()}')
        return self._running

    def mainloop(self, blocking: bool = True) -> None:
        self.start()
        if not reapy.is_inside_reaper():
            atexit.register(self._at_exit)
            while self.running():
                pass

    @reapy.inside_reaper()
    def _at_exit(self) -> None:
        self.cleanup()
        self._kill()

    @reapy.inside_reaper()
    def start(self) -> None:
        self._running = True
        self._launch()
        reapy.at_exit(self._at_exit)
        self.setup()
        self._loop()

    @reapy.inside_reaper()
    def _loop(self) -> None:
        if not RPR.ValidatePtr(self.hwnd, "HWND"):
            # self.cleanup()
            # self._kill()
            return
        try:
            self.run()
            self._handle_wm()
            reapy.defer(self._loop)
        except KeyboardInterrupt as e:
            self._kill()
            raise e

    def _handle_wm(self) -> None:
        hwnd = self.hwnd
        mess_times = self.wm_handler.message_times
        for msg, l_time in mess_times.items():
            (pOk, _, n_time, wParamLow, wParamHigh, lParamLow,
             lParamHigh) = JS.WindowMessage_Peek(hwnd, msg)
            if n_time > l_time:
                print(self.hwnd)
                print(
                    "{} || pOk:{}, time:{}, wPL:{}, wPH:{}, lPL:{}, lPH:{}".
                    format(
                        msg, pOk, n_time, wParamLow, wParamHigh, lParamLow,
                        lParamHigh
                    )
                )
                mess_times[msg] = n_time

    def setup(self) -> None:
        pass

    def run(self) -> None:
        pass

    def cleanup(self) -> None:
        pass

    @property
    def dock(self) -> int:
        ret = reapy.get_ext_state(GUI_SECTION, "%s_dock_out" % self.name)
        self._dockstate = int(float(ret))
        return self._dockstate

    @dock.setter
    def dock(self, value: int) -> None:
        self._dockstate = value
        reapy.set_ext_state(
            GUI_SECTION, "%s_dockstate" % self.name, str(value), False
        )


if __name__ == '__main__':
    try:
        root = TopLevel('my_test_window')
        root.mainloop()
    except Exception as e:
        raise e
    # hwnd = root._launch()
    # # RPR.DockWindowAddEx(hwnd, "my_test_window", "bottom", True)
    # # root.dock = 0
    # classname = JS.Window_GetClassName(root.hwnd, 100)
    # # bg = RPR.GetThemeColor("col_arrangebg", 0)
    # bg = RPR.GetThemeColor("col_main_bg", 0)
    # sbm = JS.LICE_CreateBitmap(True, root.width, root.height)
    # JS.LICE_FillRect(
    #     sbm, 0, 0, root.width, root.height, bg | 0xff000000, 1, ''
    # )
    # cOK = JS.Composite(
    #     root.hwnd, 0, 0, root.width, root.height, sbm, 0, 0, root.width,
    #     root.height
    # )
    # if RPR.ValidatePtr(root.hwnd, "HWND"):
    #     JS.Window_InvalidateRect(
    #         root.hwnd, 0, 0, root.width, root.height, True
    #     )

    # sleep(2)
    # # reapy.set_ext_state('reapy_gui', 'my_test_window', "close")
    # root._kill()
