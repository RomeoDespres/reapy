"""Fix several ReaScript API bugs.

All fixes will be applied to `reapy.reascript_api` by reapy during
the import process. Thus, this module is only intended to be used
and should not be directly used by end-users.
"""

import ctypes as ct
from reapy import reascript_api as RPR
from reapy.reascript_api import _RPR
# import typing as ty
import re

MAX_STRBUF = 4 * 1024 * 1024


def packp(t: str, v: str) -> int:
    m = re.match('^\((\w+\*|HWND)\)0x([0-9A-F]+)$', str(v))
    if (m != None):
        (_t, _v) = m.groups()
        a = int(_v[:8], 16)
        if (_t == t or t == 'void*'):
            b = int(_v[8:], 16)
            p = ct.c_uint64((a << 32) | b).value
            # if (RPR_ValidatePtr(p,t)):
            #   return p
            return p
    return 0


_RPR.rpr_packp = packp


def packs_l(
    v: str, encoding: str = "latin-1", size: int = MAX_STRBUF
) -> ct.c_char_p:
    return ct.create_string_buffer(str(v).encode(encoding), size)


def unpacks_l(
    v: ct.c_char_p,  encoding: str = 'latin-1', want_raw: bool = False
) -> str:
    s = v.value if not want_raw else v.raw
    return str(s.decode(encoding))


def MIDI_GetEvt(take, evtidx, selectedOut, mutedOut, ppqposOut, msg, msg_sz):
    a = _RPR._ft['MIDI_GetEvt']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_char_p, ct.c_void_p
    )(a)
    t = (
        _RPR.rpr_packp('MediaItem_Take*', take), ct.c_int(evtidx),
        ct.c_byte(selectedOut), ct.c_byte(mutedOut), ct.c_double(ppqposOut),
        packs_l(msg), ct.c_int(msg_sz)
    )
    r = f(
        t[0], t[1], ct.byref(t[2]), ct.byref(t[3]), ct.byref(t[4]), t[5],
        ct.byref(t[6])
    )
    return (
        r, take, evtidx, int(t[2].value), int(t[3].value), float(t[4].value),
        unpacks_l(t[5]), int(t[6].value)
    )


def MIDI_GetAllEvts(take, bufNeedBig, bufNeedBig_sz):
    a = _RPR._ft['MIDI_GetAllEvts']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_char_p, ct.c_void_p)(a)
    t = (_RPR.rpr_packp('MediaItem_Take*', take),
         packs_l(bufNeedBig, size=bufNeedBig_sz), ct.c_int(bufNeedBig_sz))
    r = f(t[0], t[1], ct.byref(t[2]))
    return (r, take, unpacks_l(t[1], want_raw=True), int(t[2].value))

# def RPR_MIDI_GetGrid(p0, p1, p2):
#     a = _ft['MIDI_GetGrid']
#     f = CFUNCTYPE(c_double, c_uint64, c_void_p, c_void_p)(a)
#     t = (rpr_packp('MediaItem_Take*', p0), c_double(p1), c_double(p2))
#     r = f(t[0], byref(t[1]), byref(t[2]))
#     return (r, p0, float(t[1].value), float(t[2].value))


def MIDI_GetHash(p0, p1, p2, p3):
    a = _RPR._ft['MIDI_GetHash']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte,
                     ct.c_char_p, ct.c_int)(a)
    t = (
        _RPR.rpr_packp('MediaItem_Take*',
                       p0), ct.c_byte(p1), packs_l(p2), ct.c_int(p3)
    )
    r = f(t[0], t[1], t[2], t[3])
    return (r, p0, p1, unpacks_l(t[2]), p3)

# def RPR_MIDI_GetNote(p0, p1, p2, p3, p4, p5, p6, p7, p8):
#     a = _ft['MIDI_GetNote']
#     f = CFUNCTYPE(
#         c_byte, c_uint64, c_int, c_void_p, c_void_p, c_void_p, c_void_p,
#         c_void_p, c_void_p, c_void_p
#     )(a)
#     t = (
#         rpr_packp('MediaItem_Take*', p0), c_int(p1), c_byte(p2), c_byte(p3),
#         c_double(p4), c_double(p5), c_int(p6), c_int(p7), c_int(p8)
#     )
#     r = f(
#         t[0], t[1], byref(t[2]), byref(t[3]), byref(t[4]), byref(t[5]),
#         byref(t[6]), byref(t[7]), byref(t[8])
#     )
#     return (
#         r, p0, p1, int(t[2].value), int(t[3].value), float(t[4].value),
#         float(t[5].value), int(t[6].value), int(t[7].value), int(t[8].value)
#     )

# def RPR_MIDI_GetScale(p0, p1, p2, p3, p4):
#     a = _ft['MIDI_GetScale']
#     f = CFUNCTYPE(c_byte, c_uint64, c_void_p, c_void_p, c_char_p, c_int)(a)
#     t = (
#         rpr_packp('MediaItem_Take*',
#                   p0), c_int(p1), c_int(p2), rpr_packs(p3), c_int(p4)
#     )
#     r = f(t[0], byref(t[1]), byref(t[2]), t[3], t[4])
#     return (r, p0, int(t[1].value), int(t[2].value), rpr_unpacks(t[3]), p4)


def MIDI_GetTextSysexEvt(p0, p1, p2, p3, p4, p5, p6, p7):
    a = _RPR._ft['MIDI_GetTextSysexEvt']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_char_p, ct.c_void_p
    )(a)
    t = (
        _RPR.rpr_packp('MediaItem_Take*',
                       p0), ct.c_int(p1), ct.c_byte(p2), ct.c_byte(p3),
        ct.c_double(p4), ct.c_int(p5), packs_l(p6, size=p7), ct.c_int(p7)
    )
    r = f(
        t[0], t[1], ct.byref(t[2]), ct.byref(
            t[3]), ct.byref(t[4]), ct.byref(t[5]), t[6],
        ct.byref(t[7])
    )
    return (
        r, p0, p1, int(t[2].value), int(t[3].value), float(t[4].value),
        int(t[5].value), unpacks_l(t[6], want_raw=False), int(t[7].value)
    )


def MIDI_GetTrackHash(p0, p1, p2, p3):
    a = _RPR._ft['MIDI_GetTrackHash']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte,
                     ct.c_char_p, ct.c_int)(a)
    t = (_RPR.rpr_packp('MediaTrack*', p0),
         ct.c_byte(p1), packs_l(p2), ct.c_int(p3))
    r = f(t[0], t[1], t[2], t[3])
    return (r, p0, p1, unpacks_l(t[2]), p3)

# def RPR_MIDI_InsertCC(p0, p1, p2, p3, p4, p5, p6, p7):
#     a = _ft['MIDI_InsertCC']
#     f = CFUNCTYPE(
#         c_byte, c_uint64, c_byte, c_byte, c_double, c_int, c_int, c_int, c_int
#     )(a)
#     t = (
#         rpr_packp('MediaItem_Take*', p0), c_byte(p1), c_byte(p2), c_double(p3),
#         c_int(p4), c_int(p5), c_int(p6), c_int(p7)
#     )
#     r = f(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])
#     return r


def MIDI_InsertEvt(take, selected, muted, ppqpos, bytestr, bytestr_sz):
    a = _RPR._ft['MIDI_InsertEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte,
                     ct.c_byte, ct.c_double, ct.c_char_p,
                     ct.c_int)(a)
    t = (
        _RPR.rpr_packp('MediaItem_Take*',   # 0
                       take),
        ct.c_byte(selected),                # 1
        ct.c_byte(muted),                   # 2
        ct.c_double(ppqpos),                # 3
        packs_l(bytestr),                   # 4
        ct.c_int(bytestr_sz)                # 5
    )
    r = f(t[0], t[1], t[2], t[3], t[4], t[5])
    return r

# def RPR_MIDI_InsertNote(p0, p1, p2, p3, p4, p5, p6, p7, p8):
#     a = _ft['MIDI_InsertNote']
#     f = CFUNCTYPE(
#         c_byte, c_uint64, c_byte, c_byte, c_double, c_double, c_int, c_int,
#         c_int, c_void_p
#     )(a)
#     t = (
#         rpr_packp('MediaItem_Take*', p0), c_byte(p1), c_byte(p2), c_double(p3),
#         c_double(p4), c_int(p5), c_int(p6), c_int(p7), c_byte(p8)
#     )
#     r = f(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], byref(t[8]))
#     return (r, p0, p1, p2, p3, p4, p5, p6, p7, int(t[8].value))


def MIDI_InsertTextSysexEvt(take, selected, muted, ppqpos,
                            type_, bytestr, bytestr_sz):
    a = _RPR._ft['MIDI_InsertTextSysexEvt']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_byte, ct.c_double,
        ct.c_int, ct.c_char_p, ct.c_int
    )(a)
    t = (
        _RPR.rpr_packp('MediaItem_Take*',   # 0
                       take),
        ct.c_byte(selected),                # 1
        ct.c_byte(muted),                   # 2
        ct.c_double(ppqpos),                # 3
        ct.c_int(type_),                    # 4
        packs_l(bytestr),                   # 5
        ct.c_int(bytestr_sz)                # 6
    )
    r = f(t[0], t[1], t[2], t[3], t[4], t[5], t[6])
    return r


def MIDI_SetAllEvts(take, buf, buf_sz):
    a = _RPR._ft['MIDI_SetAllEvts']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_char_p, ct.c_int)(a)
    t = (_RPR.rpr_packp('MediaItem_Take*', take),
         packs_l(buf, size=buf_sz), ct.c_int(buf_sz))
    r = f(t[0], t[1], t[2])
    return r


def MIDI_SetCC(take, ccidx, selected, muted, ppqpos,
               chan_msg, channel, msg2, msg3, sort):
    a = _RPR._ft['MIDI_SetCC']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p
    )(a)
    r = f(
        _RPR.rpr_packp('MediaItem_Take*', take),
        ct.c_int(ccidx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if ppqpos is None else ct.byref(ct.c_double(ppqpos)),
        None if chan_msg is None else ct.byref(ct.c_int(chan_msg)),
        None if channel is None else ct.byref(ct.c_int(channel)),
        None if msg2 is None else ct.byref(ct.c_int(msg2)),
        None if msg3 is None else ct.byref(ct.c_int(msg3)),
        None if sort is None else ct.c_byte(sort)
    )
    return r


def MIDI_SetCCShape(take, ccidx, shape, beiz_tens, no_sort):
    a = _RPR._ft['MIDI_SetCCShape']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_int,
                     ct.c_int, ct.c_double, ct.c_void_p)(a)
    r = f(_RPR.rpr_packp('MediaItem_Take*', take),
          ct.c_int(ccidx),
          ct.c_int(shape),
          ct.c_double(beiz_tens),
          None if no_sort is None else ct.byref(ct.c_byte(no_sort)))
    return r


def MIDI_SetEvt(take, evt_idx, selected, muted, ppqpos, msg, msg_sz, no_sort):
    a = _RPR._ft['MIDI_SetEvt']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_char_p, ct.c_int,
        ct.c_void_p
    )(a)
    r = f(
        _RPR.rpr_packp('MediaItem_Take*', take),
        ct.c_int(evt_idx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if ppqpos is None else ct.byref(ct.c_double(ppqpos)),
        None if msg is None else packs_l(msg),
        ct.c_int(msg_sz if msg_sz is not None else 0),
        None if no_sort is None else ct.byref(ct.c_byte(no_sort))
    )
    return r


def MIDI_SetNote(take, idx, selected, muted,
                 startppqpos, endppqpos, chan, pitch, vel, noSort):
    a = _RPR._ft['MIDI_SetNote']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p
    )(a)
    r = f(
        _RPR.rpr_packp('MediaItem_Take*', take),
        ct.c_int(idx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if startppqpos is None else ct.byref(ct.c_double(startppqpos)),
        None if endppqpos is None else ct.byref(ct.c_double(endppqpos)),
        None if chan is None else ct.byref(ct.c_int(chan)),
        None if pitch is None else ct.byref(ct.c_int(pitch)),
        None if vel is None else ct.byref(ct.c_int(vel)),
        None if noSort is None else ct.byref(ct.c_byte(noSort))
    )
    return r


def MIDI_SetTextSysexEvt(take, idx, selected, muted, ppqpos,
                         type_, msg, msg_sz, noSort):
    a = _RPR._ft['MIDI_SetTextSysexEvt']
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_char_p, ct.c_int, ct.c_void_p
    )(a)
    r = f(
        _RPR.rpr_packp('MediaItem_Take*', take),
        ct.c_int(idx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if ppqpos is None else ct.byref(ct.c_double(ppqpos)),
        None if type_ is None else ct.byref(ct.c_int(type_)),
        None if msg is None else packs_l(msg, size=msg_sz),
        ct.c_int(0) if msg_sz is None else ct.c_int(msg_sz),
        None if noSort is None else ct.byref(ct.c_byte(noSort))
    )
    return r

# def RPR_MIDI_Sort(p0):
#     a = _ft['MIDI_Sort']
#     f = CFUNCTYPE(None, c_uint64)(a)
#     t = (rpr_packp('MediaItem_Take*', p0), )
#     f(t[0])
