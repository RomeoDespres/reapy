import typing as ty
import reapy
if reapy.is_inside_reaper():
    from reapy.additional_api import packp, MAX_STRBUF, packs_l, unpacks_l
    from reaper_python import _ft
    import ctypes as ct

__all__: ty.List[str] = [
    'Byte',
    'Dialog_BrowseForFolder',
    'Composite',
]


@reapy.inside_reaper()
def Byte(pointer: str, offset: int) -> int:
    """Returns the unsigned byte at address[offset].

    Parameters
    ----------
    pointer : str
        Probably, (void*)0x...
    offset : int
        Offset is added as steps of 1 byte each.

    Returns
    -------
    int
    """
    a = _ft['JS_Byte']
    f = ct.CFUNCTYPE(ct.c_int, ct.c_uint64, ct.c_int)(a)
    out_byte = ct.c_byte(0)
    f(packp('void*', pointer), ct.c_int(offset), ct.byref(out_byte))
    return int(out_byte.value)


# (
#     retval, windowHWND, srcx, srcy, srcw, srch, sysBitmap, dstx, dsty, dstw,
#     dsth, autoUpdateOptional
# ) = JS_Composite(
#     windowHWND, srcx, srcy, srcw, srch, sysBitmap, dstx, dsty, dstw, dsth,
#     autoUpdateOptional
# )


class HWND(str):
    ...


class WindowHWND(HWND):
    ...


class sysBitmap(str):
    ...


@reapy.inside_reaper()
def Composite(
    window_hwnd: WindowHWND,
    srcx: int,
    srcy: int,
    srcw: int,
    srch: int,
    sys_bitmap: sysBitmap,
    dstx: int,
    dsty: int,
    dstw: int,
    dsth: int,
    auto_update: bool = False
) -> int:
    """
    Composites a LICE bitmap with a REAPER window.

    Notes
    -----
    * If dstw or dsth is -1, the bitmap will be stretched to fill the width
        or height of the window, respectively.
    * InvalidateRect should also be called whenever the contents of the bitmap
        contents have been changed, but not the position, to trigger
        a window update.
    * On WindowsOS, the key to reducing flickering is to slow down the
        frequency at which the window is re-drawn.
        InvalidateRect should only be called when absolutely necessary,
        preferably not more than 10 times per second.
        (Also refer to the JS_Composite_Delay function.)
    * On WindowsOS, flickering can further be reduced by keeping the
        invalidated area as small as possible, covering only the bitmaps
        that have been edited or moved. However, if numerous bitmaps are
        spread over the entire window, it may be faster to simply invalidate
        the entire client area.
    * This function should not be applied directly to top-level windows,
        but rather to child windows.
    * Some classes of UI elements, particularly buttons, do not take kindly
        to being composited, and may crash REAPER.
    * On WindowsOS, GDI blitting does not perform alpha multiplication of
        the source bitmap. For proper color rendering, a separate
        pre-multiplication step is therefore required,
        using either LICE_Blit or LICE_ProcessRect.

    Parameters
    ----------
    window_hwnd : WindowHWND
    srcx : int
    srcy : int
    srcw : int
    srch : int
    sys_bitmap : sysBitmap
    dstx : int
    dsty : int
    dstw : int
    dsth : int
    auto_update : bool, optional
        If true, JS_Composite will automatically invalidate and re-draw
        the part of the window that covers the current position of the bitmap,
        and if the bitmap is being moved, also the previous position.
        (If only one or a handful of bitmaps are being moved across the screen,
        autoUpdate should result in smoother animation on WindowsOS;
        if numerous bitmaps are spread over the entire window,
        it may be faster to disable autoUpdate and instead call
        JS_Window_InvalidateRect explicitly once all bitmaps have been moved.)

    Returns
    -------
    int
        1 if successful, otherwise:
        -1 = windowHWND is not a window,
        -3 = Could not obtain the original window process,
        -4 = sysBitmap is not a LICE bitmap,
        -5 = sysBitmap is not a system bitmap,
        -6 = Could not obtain the window HDC.
    """
    a = _ft['JS_Composite']
    f = ct.CFUNCTYPE(
        ct.c_int, ct.c_uint64, ct.c_int, ct.c_int, ct.c_int, ct.c_int,
        ct.c_uint64, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_byte
    )(a)
    r = f(
        packp('(HWND)', window_hwnd), ct.c_int(srcx), ct.c_int(srcy),
        ct.c_int(srcw), ct.c_int(srch), packp('(HWND)', sys_bitmap),
        ct.c_int(dstx), ct.c_int(dsty), ct.c_int(dstw), ct.c_int(dsth),
        ct.c_byte(auto_update)
    )
    return int(r)


@reapy.inside_reaper()
def Dialog_BrowseForFolder(
    caption: str, initialFolder: str, size: int = 1000
) -> ty.Tuple[int, str]:
    a = _ft['JS_Dialog_BrowseForFolder']
    f = ct.CFUNCTYPE(
        ct.c_int, ct.c_char_p, ct.c_char_p, ct.c_char_p, ct.c_int
    )(a)
    out_folder = packs_l('v: str', encoding='utf-8', size=size)
    r = f(
        packs_l(caption, encoding='utf-8', size=len(caption)),
        packs_l(initialFolder, encoding='utf-8', size=len(initialFolder)),
        out_folder, ct.c_int(size)
    )
    return (r, unpacks_l(out_folder, encoding='utf-8'))
