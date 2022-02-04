"""Fix several ReaScript API bugs.

All fixes will be applied to `reapy.reascript_api` by reapy during
the import process. Thus, this module is only intended to be used
internally and should not be directly used by end-users.
"""

import ctypes as ct
import re

import reapy
from reapy.reascript_api import _RPR


MAX_STRBUF = 4 * 1024 * 1024


def packp(t, v):
    m = re.match(r"^\((\w+\*|HWND)\)0x([0-9A-F]+)$", str(v))
    if m is not None:
        (_t, _v) = m.groups()
        if (_t == t or t == "void*"):
            a = int(_v[:8], 16)
            b = int(_v[8:], 16)
            p = ct.c_uint64((a << 32) | b).value
            return p
    return 0


_RPR.rpr_packp = packp


def packs_l(v, encoding="latin-1", size=MAX_STRBUF):
    return ct.create_string_buffer(str(v).encode(encoding), size)


def unpacks_l(v,  encoding="latin-1", want_raw=False):
    s = v.value if not want_raw else v.raw
    return str(s.decode(encoding))


def MIDI_GetEvt(take, evtidx, selectedOut, mutedOut, ppqposOut, msg, msg_sz):
    address = _RPR._ft["MIDI_GetEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_char_p, ct.c_void_p
    )(address)
    c_selected = ct.c_byte(selectedOut)
    c_muted = ct.c_byte(mutedOut)
    c_ppq_position = ct.c_double(ppqposOut)
    c_msg = packs_l(msg, size=msg_sz)
    c_msg_length = ct.c_int(msg_sz)
    success = f(
        _RPR.rpr_packp("MediaItem_Take*", take), ct.c_int(evtidx),
        ct.byref(c_selected), ct.byref(c_muted), ct.byref(c_ppq_position),
        c_msg, ct.byref(c_msg_length)
    )
    msg_length = c_msg_length.value
    msg = unpacks_l(c_msg, want_raw=True)[:msg_length]
    return (
        success, take, evtidx, c_selected.value, c_muted.value,
        c_ppq_position.value, msg, msg_length
    )


def MIDI_GetAllEvts(take, bufNeedBig, bufNeedBig_sz):
    address = _RPR._ft["MIDI_GetAllEvts"]
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_char_p, ct.c_void_p)(address)
    c_msg = packs_l(bufNeedBig, size=bufNeedBig_sz)
    c_msg_length = ct.c_int(bufNeedBig_sz)
    success = f(
        _RPR.rpr_packp("MediaItem_Take*", take), c_msg, ct.byref(c_msg_length)
    )
    msg_length = c_msg_length.value
    msg = unpacks_l(c_msg, want_raw=True)[:msg_length]
    return success, take, msg, msg_length


def MIDI_GetHash(p0, p1, p2, p3):
    a = _RPR._ft["MIDI_GetHash"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_byte,  ct.c_char_p, ct.c_int
    )(a)
    t = (
        _RPR.rpr_packp("MediaItem_Take*", p0), ct.c_byte(p1), packs_l(p2),
        ct.c_int(p3)
    )
    r = f(*t)
    return r, p0, p1, unpacks_l(t[2]), p3


def MIDI_GetTextSysexEvt(p0, p1, p2, p3, p4, p5, p6, p7):
    address = _RPR._ft["MIDI_GetTextSysexEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_char_p, ct.c_void_p
    )(address)
    c_selected = ct.c_byte(p2)
    c_muted = ct.c_byte(p3)
    c_ppq_position = ct.c_double(p4)
    c_type = ct.c_int(p5)
    c_msg = packs_l(p6, size=p7)
    c_msg_length = ct.c_int(p7)
    success = f(
        _RPR.rpr_packp("MediaItem_Take*", p0), ct.c_int(p1),
        ct.byref(c_selected), ct.byref(c_muted), ct.byref(c_ppq_position),
        ct.byref(c_type), c_msg, ct.byref(c_msg_length)
    )
    msg_length = c_msg_length.value
    msg = unpacks_l(c_msg, want_raw=True)[:msg_length]
    return (
        success, p0, p1, c_selected.value, c_muted.value, c_ppq_position.value,
        c_type.value, msg, msg_length
    )


def MIDI_GetTrackHash(p0, p1, p2, p3):
    a = _RPR._ft["MIDI_GetTrackHash"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_char_p, ct.c_int
    )(a)
    t = (
        _RPR.rpr_packp("MediaTrack*", p0), ct.c_byte(p1), packs_l(p2),
        ct.c_int(p3)
    )
    r = f(*t)
    return r, p0, p1, unpacks_l(t[2]), p3


def MIDI_InsertEvt(take, selected, muted, ppqpos, bytestr, bytestr_sz):
    a = _RPR._ft["MIDI_InsertEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_byte, ct.c_double, ct.c_char_p,
        ct.c_int
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        ct.c_byte(selected),
        ct.c_byte(muted),
        ct.c_double(ppqpos),
        packs_l(bytestr),
        ct.c_int(bytestr_sz)
    )


def MIDI_InsertTextSysexEvt(
    take, selected, muted, ppqpos, type_, bytestr, bytestr_sz
):
    a = _RPR._ft["MIDI_InsertTextSysexEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_byte, ct.c_double,
        ct.c_int, ct.c_char_p, ct.c_int
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        ct.c_byte(selected),
        ct.c_byte(muted),
        ct.c_double(ppqpos),
        ct.c_int(type_),
        packs_l(bytestr),
        ct.c_int(bytestr_sz)
    )


def MIDI_SetAllEvts(take, buf, buf_sz):
    a = _RPR._ft["MIDI_SetAllEvts"]
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_char_p, ct.c_int)(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        packs_l(buf, size=buf_sz),
        ct.c_int(buf_sz)
    )


def MIDI_SetCC(
    take, ccidx, selected, muted, ppqpos, chan_msg, channel, msg2, msg3, sort
):
    a = _RPR._ft["MIDI_SetCC"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_void_p
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
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


def MIDI_SetCCShape(take, ccidx, shape, beiz_tens, no_sort):
    a = _RPR._ft["MIDI_SetCCShape"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_int, ct.c_double, ct.c_void_p
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        ct.c_int(ccidx),
        ct.c_int(shape),
        ct.c_double(beiz_tens),
        None if no_sort is None else ct.byref(ct.c_byte(no_sort))
    )


def MIDI_SetEvt(take, evt_idx, selected, muted, ppqpos, msg, msg_sz, no_sort):
    a = _RPR._ft["MIDI_SetEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_char_p, ct.c_int, ct.c_void_p
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        ct.c_int(evt_idx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if ppqpos is None else ct.byref(ct.c_double(ppqpos)),
        None if msg is None else packs_l(msg),
        ct.c_int(msg_sz if msg_sz is not None else 0),
        None if no_sort is None else ct.byref(ct.c_byte(no_sort))
    )


def MIDI_SetNote(
    take, idx, selected, muted, startppqpos, endppqpos, chan, pitch, vel,
    noSort
):
    a = _RPR._ft["MIDI_SetNote"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p,
        ct.c_void_p
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
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


def MIDI_SetTextSysexEvt(
    take, idx, selected, muted, ppqpos, type_, msg, msg_sz, noSort
):
    a = _RPR._ft["MIDI_SetTextSysexEvt"]
    f = ct.CFUNCTYPE(
        ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_void_p, ct.c_void_p, ct.c_char_p, ct.c_int, ct.c_void_p
    )(a)
    return f(
        _RPR.rpr_packp("MediaItem_Take*", take),
        ct.c_int(idx),
        None if selected is None else ct.byref(ct.c_byte(selected)),
        None if muted is None else ct.byref(ct.c_byte(muted)),
        None if ppqpos is None else ct.byref(ct.c_double(ppqpos)),
        None if type_ is None else ct.byref(ct.c_int(type_)),
        None if msg is None else packs_l(msg, size=msg_sz),
        ct.c_int(0) if msg_sz is None else ct.c_int(msg_sz),
        None if noSort is None else ct.byref(ct.c_byte(noSort))
    )


@reapy.inside_reaper()
def ValidatePtr2(p0, p1, p2):
    a = _RPR._ft["ValidatePtr2"]
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_uint64, ct.c_char_p)(a)
    project = _RPR.rpr_packp("ReaProject*", p0)
    pointer = ct.c_uint64(p1)
    name = _RPR.rpr_packsc(p2)
    return f(project, pointer, name)


def GetTrackMIDINoteName(track_idx: int, pitch: int, chan: int) -> str:
    a = _RPR._ft['GetTrackMIDINoteName']
    f = ct.CFUNCTYPE(ct.c_char_p, ct.c_int, ct.c_int, ct.c_int)(a)
    t = (ct.c_int(track_idx), ct.c_int(pitch), ct.c_int(chan))
    r = f(t[0], t[1], t[2])
    return '' if not r else str(r.decode())


def GetTrackMIDINoteNameEx(
    project: str, track: str, pitch: int, chan: int
) -> str:
    a = _RPR._ft['GetTrackMIDINoteNameEx']
    f = ct.CFUNCTYPE(
        ct.c_char_p, ct.c_uint64, ct.c_uint64, ct.c_int, ct.c_int
    )(a)
    t = (
        packp('ReaProject*',
              project), packp('MediaTrack*',
                              track), ct.c_int(pitch), ct.c_int(chan)
    )
    r = f(t[0], t[1], t[2], t[3])
    return '' if not r else str(r.decode())
