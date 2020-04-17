import ctypes as ct
from reapy import reascript_api as RPR
from reapy.reascript_api import _RPR


def packs_l(v: str) -> ct.c_char_p:
    MAX_STRBUF = 4*1024*1024
    return ct.create_string_buffer(str(v).encode("latin-1"), MAX_STRBUF)


def unpacks_l(v):
    return str(v.value.decode('latin-1'))


def MIDI_GetEvt(take, evtidx, selectedOut, mutedOut, ppqposOut, msg, msg_sz):
    a = _RPR._ft['MIDI_GetEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p,
                     ct.c_void_p, ct.c_void_p, ct.c_char_p, ct.c_void_p)(a)
    t = (_RPR.rpr_packp('MediaItem_Take*', take), ct.c_int(evtidx), ct.c_byte(selectedOut),
         ct.c_byte(mutedOut), ct.c_double(ppqposOut), packs_l(msg), ct.c_int(msg_sz))
    r = f(t[0], t[1], ct.byref(t[2]), ct.byref(t[3]),
          ct.byref(t[4]), t[5], ct.byref(t[6]))
    return (r, take, evtidx, int(t[2].value), int(t[3].value),
            float(t[4].value), unpacks_l(t[5]), int(t[6].value))
