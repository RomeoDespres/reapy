from reapy.core.track.track import RecMonitor
import pytest as pt


def test_rec_monitor():
    with pt.raises(TypeError, match=r'cannot.+track.*'):
        RecMonitor.off | RecMonitor.normal
    with pt.raises(TypeError, match=r'cannot.+track.*'):
        RecMonitor.off | RecMonitor.not_while_play
    with pt.raises(TypeError, match=r'cannot.+track.*'):
        RecMonitor.normal | RecMonitor.not_while_play
    with pt.raises(TypeError, match=r'cannot.+item.*'):
        RecMonitor.items_rec_off | RecMonitor.items_rec_on
    with pt.raises(TypeError, match=r'use flag\.value instead'):
        RecMonitor.items_rec_off | 0b001001001
    comb1 = RecMonitor.items_rec_off.value | 0b001001000
    assert comb1 == 0b001001001
    comb = RecMonitor.items_rec_off | RecMonitor.normal
    assert comb & RecMonitor.items_rec_off == RecMonitor.items_rec_off
    assert comb & RecMonitor.normal == RecMonitor.normal

    assert RecMonitor._resolve_flags(comb) == (1, 0)
    assert RecMonitor._resolve_flags(RecMonitor.items_rec_on) == (None, 1)
    assert RecMonitor._resolve_flags(RecMonitor.off) == (0, None)

