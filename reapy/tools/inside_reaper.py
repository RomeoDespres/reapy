import reapy
if not reapy.is_inside_reaper():
    from . import dist_program


class InsideReaper:

    """
    Context manager for efficient calls from outside REAPER.

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
    """

    def __enter__(self):
        if not reapy.is_inside_reaper():
            dist_program.Program("HOLD").run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not reapy.is_inside_reaper():
            dist_program.Program("RELEASE").run()
        return False
