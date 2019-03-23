import reapy
from reapy.core import ReapyObject
import reapy.reascript_api as RPR


class Window(ReapyObject):

    def __init__(self, id):
        self.id = id

    @property
    def _args(self):
        return (self.id,)

    def refresh(self):
        """Refresh window."""
        RPR.DockWindowRefreshForHWND(self.id)
