import reapy.reascript_api as RPR
from .window import Window


class ToolTip(Window):

    """Tooltip window."""

    def __init__(self, message=" ", x=0, y=0, topmost=True, show=True):
        """Initialize tooltip.

        Parameters
        ----------
        message : str, optional
            ToolTip message (default=" "). Note that tooltips with
            empty messages are always hidden.
        x : int, optional
            x position (default=0).
        y : int, optional
            y position (default=0).
        topmost : bool, optional
            Whether tooltip should be displayed on top of all other
            windows (default=True).
        show : bool, optional
            Whether to show tooltip on initialization (default=True).
        """
        self._message = message
        self._x = x
        self._y = y
        self._topmost = topmost
        if show:
            self.show()
        self.id = RPR.GetTooltipWindow

    def hide(self):
        """Hide tooltip."""
        RPR.TrackCtl_SetToolTip("", self.x, self.y, self.topmost)
        self._is_shown = False

    @property
    def message(self):
        """
        Tooltip message.

        Note that tooltips with empty messages are always hidden.

        :type: str
        """
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
        if self._is_shown:
            self.show()

    def refresh(self):
        pass

    def show(self):
        """Show tooltip."""
        RPR.TrackCtl_SetToolTip(self.message, self.x, self.y, self.topmost)
        self._is_shown = True

    @property
    def topmost(self):
        """
        Whether tooltip is displayed on top of all other windows.

        :type: bool
        """
        return self._topmost

    @topmost.setter
    def topmost(self, topmost):
        self._topmost = topmost
        if self._is_shown:
            self.show()

    @property
    def x(self):
        """
        x position.

        :type: int"""
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        if self._is_shown:
            self.show()

    @property
    def y(self):
        """y position.

        :type: int
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        if self._is_shown:
            self.show()
