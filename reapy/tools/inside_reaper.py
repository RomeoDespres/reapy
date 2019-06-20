import contextlib

import reapy
if not reapy.is_inside_reaper():
    from . import dist_program


class InsideReaper(contextlib.ContextDecorator):

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

    def __enter__(self):
        if not reapy.is_inside_reaper():
            dist_program.Program("HOLD").run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not reapy.is_inside_reaper():
            dist_program.Program("RELEASE").run()
        return False
