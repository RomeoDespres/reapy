import reapy
if not reapy.is_inside_reaper():
    from . import dist_program


class InsideReaper:

    def __enter__(self):
        if not reapy.is_inside_reaper():
            dist_program.Program("HOLD").run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not reapy.is_inside_reaper():
            dist_program.Program("RELEASE").run()
        return False
