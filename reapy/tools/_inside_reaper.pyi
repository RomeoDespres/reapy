import contextlib
import functools
import typing as ty

import reapy
import reapy.config
from reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning
if not reapy.is_inside_reaper():
    try:
        from .network import Client, WebInterface
        _WEB_INTERFACE = WebInterface(reapy.config.WEB_INTERFACE_PORT)
        _CLIENT = Client(_WEB_INTERFACE.get_reapy_server_port())
    except DisabledDistAPIError:
        import warnings
        warnings.warn(DisabledDistAPIWarning())
        _CLIENT = None

FuncType = ty.Callable[..., ty.Any]
F = ty.TypeVar('F', bound=FuncType)


def dist_api_is_enabled() -> bool:
    """Return whether reapy can reach REAPER from the outside."""
    ...


class inside_reaper(contextlib.ContextDecorator):
    """
    Context manager for efficient calls from outside REAPER.

    It can also be used as a function decorator.

    Examples
    --------
    Instead of running:

    >>> project = reapy.Project()
    >>> l = [project.bpm for i in range(1000)

    which takes around 30 seconds, run:

    >>> project = reapy.Project()
    >>> with reapy.inside_reaper():
    ...     l = [project.bpm for i in range(1000)
    ...

    which takes 0.1 seconds!

    Example usage as decorator:

    >>> @reapy.inside_reaper()
    ... def add_n_tracks(n):
    ...     for x in range(n):
    ...         reapy.Project().add_track()

    """

    def __call__(self,
                 func: F,
                 encoded_func: ty.Optional[ty.Dict[str, object]] = None
                 ) -> ty.Callable[..., contextlib.ContextManager[None]]:
        ...

    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:  # type: ignore
        ...


class DistProperty(property):

    _inside_reaper: inside_reaper

    @classmethod
    def from_property(cls, p: property) -> property:
        ...

    @staticmethod
    def _encode(f: ty.Callable[..., ty.Any],
                method_name: str) -> ty.Dict[str, object]:
        ...

    def getter(self, fget: F) -> property:
        ...

    def setter(self, fset: F) -> property:
        ...

    def deleter(self, fdel: F) -> property:
        ...


def reconnect() -> None:
    """
    Reconnect to REAPER ReaScript API.

    This function has no effect from inside REAPER.

    Examples
    --------
    Assume no REAPER instance is active.
    >>> import reapy
    DisabledDistAPIWarning: Can't reach distant API. Please start REAPER, or
    call reapy.config.enable_dist_api() from inside REAPER to enable distant
    API.
      warnings.warn(DisabledDistAPIWarning())
    >>> p = reapy.Project()  # Results in error
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "C:\\Users\\despres\\Desktop\\reaper\\scripts\\reapy\\reapy\\core\\project\\project.py", line 26, in __init__
        id = RPR.EnumProjects(index, None, 0)[0]
    AttributeError: module 'reapy.reascript_api' has no attribute 'EnumProjects'
    >>> # Now start REAPER
    ...
    >>> reapy.reconnect()
    >>> p = reapy.Project()  # No error!
    """
    ...
