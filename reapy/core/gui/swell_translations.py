"""Module holds constants defined in WDL SWELL.

While the development is going under Linux — «Swell is the new Win32»
I'm not sure it behaves exactly like Win32, but untill proven otherwise —
Swell constants are used just as «Pure Win32».
"""
from enum import IntFlag, IntEnum
import platform


class vNumKey(IntEnum):
    """Additional enum for numpad keys."""
    NUMPAD0 = 0x60
    NUMPAD1 = 0x61
    NUMPAD2 = 0x62
    NUMPAD3 = 0x63
    NUMPAD4 = 0x64
    NUMPAD5 = 0x65
    NUMPAD6 = 0x66
    NUMPAD7 = 0x67
    NUMPAD8 = 0x68
    NUMPAD9 = 0x69
    MULTIPLY = 0x6A
    ADD = 0x6B
    SEPARATOR = 0x6C
    SUBTRACT = 0x6D
    DECIMAL = 0x6E
    DIVIDE = 0x6F

    def char(self) -> str:
        table = {
            vNumKey.NUMPAD0: "0",
            vNumKey.NUMPAD1: "1",
            vNumKey.NUMPAD2: "2",
            vNumKey.NUMPAD3: "3",
            vNumKey.NUMPAD4: "4",
            vNumKey.NUMPAD5: "5",
            vNumKey.NUMPAD6: "6",
            vNumKey.NUMPAD7: "7",
            vNumKey.NUMPAD8: "8",
            vNumKey.NUMPAD9: "9",
            vNumKey.MULTIPLY: "*",
            vNumKey.ADD: "+",
            vNumKey.SEPARATOR: ",",
            vNumKey.SUBTRACT: "-",
            vNumKey.DECIMAL: ".",
            vNumKey.DIVIDE: "/",
        }
        return table[self]

    def __repr__(self) -> str:
        return "<vNumKey.{}: {}>".format(self.name, hex(self.value))


class vVirtKey(IntFlag):
    """Virtual (modifer) keys flags."""

    # FVIRTKEY = 1

    SHIFT = 0x04
    CONTROL = 0x08
    ALT = 0x10
    LWIN = 0x20


class vKey(IntEnum):
    """Swell vKeys translation table.

    Swell (and, I really hope, WDL) use its own vKeys mapping being slight
    different than Win32.
    """
    # LBUTTON = 0x01
    # RBUTTON = 0x02
    # MBUTTON = 0x04
    BACK = 0x08
    TAB = 0x09
    CLEAR = 0x0C
    RETURN = 0x0D
    SHIFT = 0x10
    CONTROL = 0x11
    # MENU = 0x12
    # ALT is missing in normal vKeys, but MENU takes its place on Linux
    ALT = 0x12
    PAUSE = 0x13
    CAPITAL = 0x14
    ESCAPE = 0x1B
    SPACE = 0x20
    PRIOR = 0x21
    NEXT = 0x22
    END = 0x23
    HOME = 0x24
    LEFT = 0x25
    UP = 0x26
    RIGHT = 0x27
    DOWN = 0x28
    SELECT = 0x29
    PRINT = 0x2A
    SNAPSHOT = 0x2C
    INSERT = 0x2D
    DELETE = 0x2E
    HELP = 0x2F
    LWIN = 0x5B
    NUMPAD0 = 0x60
    NUMPAD1 = 0x61
    NUMPAD2 = 0x62
    NUMPAD3 = 0x63
    NUMPAD4 = 0x64
    NUMPAD5 = 0x65
    NUMPAD6 = 0x66
    NUMPAD7 = 0x67
    NUMPAD8 = 0x68
    NUMPAD9 = 0x69
    MULTIPLY = 0x6A
    ADD = 0x6B
    SEPARATOR = 0x6C
    SUBTRACT = 0x6D
    DECIMAL = 0x6E
    DIVIDE = 0x6F
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F18 = 0x81
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87
    NUMLOCK = 0x90
    SCROLL = 0x91

    def __repr__(self) -> str:
        return "<vKey.{}: {}>".format(self.name, hex(self.value))


class WS(IntFlag):
    """Window Styles as hex."""
    # only used by GetWindowLong(GWL_STYLE) -- not settable
    VISIBLE = 0x02000000

    CHILD = 0x40000000
    DISABLED = 0x08000000
    CLIPSIBLINGS = 0x04000000
    CAPTION = 0x00C00000
    VSCROLL = 0x00200000
    HSCROLL = 0x00100000
    SYSMENU = 0x00080000
    THICKFRAME = 0x00040000
    GROUP = 0x00020000
    TABSTOP = 0x00010000
