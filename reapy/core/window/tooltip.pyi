import reapy.reascript_api as RPR
from .window import Window


class ToolTip(Window):
    """Tooltip window."""
    id: bytes
    _x: int
    _y: int
    _topmost: bool
    _show: bool

    def __init__(self,
                 message: str = " ",
                 x: int = 0,
                 y: int = 0,
                 topmost: bool = True,
                 show: bool = True) -> None:
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
        ...

    def hide(self) -> None:
        """Hide tooltip."""
        ...

    @property
    def message(self) -> str:
        """
        Tooltip message.

        Note that tooltips with empty messages are always hidden.

        :type: str
        """
        ...

    @message.setter
    def message(self, message: str) -> None:
        ...

    def refresh(self) -> None:
        ...

    def show(self) -> None:
        """Show tooltip."""
        ...

    @property
    def topmost(self) -> bool:
        """
        Whether tooltip is displayed on top of all other windows.

        :type: bool
        """
        ...

    @topmost.setter
    def topmost(self, topmost: bool) -> None:
        ...

    @property
    def x(self) -> int:
        """
        x position.

        :type: int"""
        ...

    @x.setter
    def x(self, x: int) -> None:
        ...

    @property
    def y(self) -> int:
        """y position.

        :type: int
        """
        ...

    @y.setter
    def y(self, y: int) -> None:
        ...
