import reapy
from reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning

import warnings

if not reapy.is_inside_reaper():
    try:
        from reapy.reascript_api.network import Client, WebInterface
        from reapy.config.config import WEB_INTERFACE_PORT
        WEB_INTERFACE = WebInterface(WEB_INTERFACE_PORT)
        CLIENT = Client(WEB_INTERFACE.get_reapy_server_port())
    except DisabledDistAPIError:
        warnings.warn(DisabledDistAPIWarning())

from . import program


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
            return super(DistProgram, self).run(**input)
        else:
            return CLIENT.run_program(self, input)