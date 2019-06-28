"""Define distant Program class."""
import functools

import reapy
from reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning
from . import program

if not reapy.is_inside_reaper():
    try:
        from reapy.reascript_api.network import Client, WebInterface
        WEB_INTERFACE = WebInterface(reapy.config.WEB_INTERFACE_PORT)
        CLIENT = Client(WEB_INTERFACE.get_reapy_server_port())
    except DisabledDistAPIError:
        import warnings
        warnings.warn(DisabledDistAPIWarning())


class Program(program.Program):

    @staticmethod
    def from_function(function_name):
        code = "result = {}(*args, **kwargs)".format(function_name)
        program = Program(code, "result")

        def g(*args, **kwargs):
            return program.run(args=args, kwargs=kwargs)[0]

        return g

    def run(self, **input):
        if reapy.is_inside_reaper():
            return super(Program, self).run(**input)
        else:
            return CLIENT.run_program(self, input)

    @staticmethod
    def run_inside(func):
        """Decorator to make a function/method executable inside Reaper
            when called from an external app.

            Should only be able to be called from outside Reaper.
            Parent class' method does not actually decorate `func`.

            TODO: support wrapping property getters/setters if possible.
        """
        # check if the decorated function is inside reapy
        func_module = func.__module__
        if func_module != 'reapy' and not func_module.startswith('reapy.'):
            raise RuntimeError('Cannot decorate non-reapy function/method!')
        # TODO: support decorating non-reapy code some day

        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            program = Program(func, None)
            return program.run(args=args, kwargs=kwargs)
        return _wrap
