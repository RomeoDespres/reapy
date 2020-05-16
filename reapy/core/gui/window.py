import typing as ty
import os
from time import sleep

import reapy
from reapy import JS
from reapy import reascript_api as RPR
from reapy.core import ReapyObject

GUI_SECTION = "reapy_gui"

_lua_template = """
gfx.init("{name}", {x}, {y}, {dockstate}, {width}, {height})
function main()
    ext_dock = reaper.GetExtState("{ext_sect}", "{name}_dockstate")
    if ext_dock ~= "" then
        gfx.dock(tonumber(ext_dock))
        reaper.SetExtState("{ext_sect}", "{name}_dockstate", "", false)
    end
    reaper.SetExtState("{ext_sect}", "{name}_dock_out",
        tostring(gfx.dock(-1)), false)
    gfx.update()
    if reaper.GetExtState("{ext_sect}", "{name}") ~= "close" then
        reaper.defer(main)
    else
        reaper.SetExtState("{ext_sect}", "{name}", "", false)
        -- reaper.ShowConsoleMsg(gfx.x)
        -- reaper.ShowConsoleMsg(gfx.y)
        -- reaper.ShowConsoleMsg(gfx.w)
        -- reaper.ShowConsoleMsg(gfx.h)
    end
end
main()
"""


class TopLevel(ReapyObject):

    def __init__(
        self,
        name: str,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        dockstate: int = 1
    ) -> None:
        self.name, self.x, self.y, self.width, self.height, self._dockstate = (
            name, x, y, width, height, dockstate
        )
        self.filename = "{}_gui.lua".format(name)
        self._hwnd: ty.Optional[JS.VoidPtr] = None

    @property
    def hwnd(self) -> JS.VoidPtr:
        if self._hwnd is None:
            raise RuntimeError('Window is not initialized')
        return self._hwnd

    @reapy.inside_reaper()
    def _launch(self) -> JS.VoidPtr:
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
        ret, array = JS.Window_ArrayFindEx(self.name, True)
        if ret == -1:
            raise RuntimeError("can not find gui window")
        self._hwnd = JS.reaper_array_to_hwnd(array)[0]
        ret, l, t, r, b = JS.Window_GetRect(self.hwnd)
        if ret:
            self.x, self.y, self.width, self.height = l, t, r - l, b - t
            print(self.x, self.y, self.width, self.height)
        return self.hwnd

    @reapy.inside_reaper()
    def _kill(self) -> None:
        reapy.set_ext_state(GUI_SECTION, self.name, "close")
        reapy.remove_reascript(self.filename)
        os.remove(self.filename)

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
    root = TopLevel('my_test_window')
    hwnd = root._launch()
    print(hwnd)
    print(JS.Window_GetRect(hwnd))
    # RPR.DockWindowAddEx(hwnd, "my_test_window", "bottom", True)
    # root.dock = 0
    print(root.dock)
    classname = JS.Window_GetClassName(root.hwnd, 100)
    # bg = RPR.GetThemeColor("col_arrangebg", 0)
    bg = RPR.GetThemeColor("col_main_bg", 0)
    print(f"bg:{hex(bg)}")
    sbm = JS.LICE_CreateBitmap(True, root.width, root.height)
    JS.LICE_FillRect(
        sbm, 0, 0, root.width, root.height, bg | 0xff000000, 1, ''
    )
    cOK = JS.Composite(
        root.hwnd, 0, 0, root.width, root.height, sbm, 0, 0, root.width,
        root.height
    )
    print(cOK)
    if RPR.ValidatePtr(root.hwnd, "HWND"):
        JS.Window_InvalidateRect(
            root.hwnd, 0, 0, root.width, root.height, True
        )

    sleep(2)
    # reapy.set_ext_state('reapy_gui', 'my_test_window', "close")
    root._kill()
