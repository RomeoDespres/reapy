"""Define reapy.defer and reapy.at_exit."""

import reapy

import os
import sys
import tempfile
import typing as ty


class Deferrer:
    """Class to register and run deferred calls."""

    _next_call_id: int
    _callbacks: ty.Dict[int, ty.Callable[..., ty.Any]]
    _args: ty.Dict[int, ty.Tuple[ty.Any, ...]]
    _kwargs: ty.Dict[int, ty.Dict[str, ty.Any]]

    def _get_new_call_id(self) -> int:
        ...

    def _wrapped_open(self, *args: ty.Any,
                      **kwargs: ty.Any) -> ty.Union[ReaperConsole, ty.Any]:
        ...

    def defer(self,
              callback: ty.Callable[..., ty.Any],
              args: ty.Tuple[ty.Any, ...],
              kwargs: ty.Dict[str, ty.Any],
              at_exit: bool = False) -> None:
        ...

    def run(self, call_id: int) -> None:
        ...


class ReaperConsole:
    """File-like wrapper around the Reaper Console."""
    def close(self) -> None:
        ...

    def flush(self) -> None:
        ...

    def write(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...


def at_exit(f: ty.Callable[..., ty.Any], *args: ty.Any,
            **kwargs: ty.Any) -> None:
    """
    Make REAPER call a function after script execution.

    The function is also called if excution is terminated by user.

    Parameters
    ----------
    f : callable
        Function to be called later.
    args : tuple, optional
        Positional arguments to pass to ``f``.
    kwargs : dict, optional
        Keyword arguments to pass to ``f``.

    Raises
    ------
    AssertionError
        When called from outside REAPER.

    Examples
    --------
    Typical use case of ``at_exit`` is cleaning up after a ``defer``
    loop.

    The following example opens a file and starts a loop that
    indefinitely writes integers to that file. Since we want the file
    to be closed when the user terminates script execution, call to
    its ``close`` method is deferred to ``reapy.at_exit``.

    >>> import reapy
    >>> file = open("somefile.txt", "w")
    >>> def stupid_loop(i):
    ...     file.write(i)
    ...     reapy.defer(stupid_loop, i + 1)
    ...
    >>> reapy.at_exit(file.close)
    >>> stupid_loop(0)
    """
    ...


def defer(f: ty.Callable[..., ty.Any], *args: ty.Any,
          **kwargs: ty.Any) -> None:
    """
    Make REAPER call a function later.

    Parameters
    ----------
    f : callable
        Function to be called later.
    args : tuple, optional
        Positional arguments to pass to ``f``.
    kwargs : dict, optional
        Keyword arguments to pass to ``f``.

    Raises
    ------
    AssertionError
        When called from outside REAPER.

    Notes
    -----
    The average time before a defered call is actually run is about
    0.03 seconds (around 30 defered calls are allowed per second).

    Examples
    --------
    Typical use case of ``defer`` is running loops that don't block
    REAPER GUI.

    The following example creates a loop that indefinitely prints
    integers to the REAPER console, without blocking REAPER GUI.

    >>> import reapy
    >>> def stupid_loop(i):
    ...     reapy.print(i)
    ...     reapy.defer(stupid_loop, i + 1)
    ...
    >>> stupid_loop(0)
    """
    # Check we are inside REAPER
    ...
