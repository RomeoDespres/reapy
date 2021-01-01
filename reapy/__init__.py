import sys


def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.

    If ``reapy`` is run from inside a REAPER instance but currently
    controls another REAPER instance on a slave machine (with
    ``reapy.connect``), return False.
    """
    inside = hasattr(sys.modules["__main__"], "obj")
    if not inside:
        return False
    else:
        try:
            return machines.get_selected_machine_host() is None
        except NameError:
            # machines is undefined because we are still in the initial
            # import process.
            return True



from .tools import (
    connect, connect_to_default_machine, dist_api_is_enabled, inside_reaper,
    reconnect
)
from . import reascript_api
from .config import configure_reaper
from .core import (
    # from .reapy_object
    ReapyObject,
    ReapyObjectList,
    # from .project
    Marker,
    Project,
    Region,
    TimeSelection,
    # from .audio_accessor
    AudioAccessor,
    # from .envelope
    Envelope,
    EnvelopeList,
    EnvelopePoint,
    # from .fx
    FX,
    FXList,
    FXParam,
    FXParamsList,
    # from .item
    CC,
    CCList,
    Item,
    Note,
    NoteList,
    Source,
    Take,
    # from .track
    AutomationItem,
    Send,
    Track,
    TrackList,
    # from .window
    MIDIEditor,
    ToolTip,
    Window,
)
from .core.reaper import *


__version__ = "0.10.0"
