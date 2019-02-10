import reapy

if reapy.is_inside_reaper():
    from reaper_python import *
else:
    from .network import Client, WebInterface
    from reapy.config.config import DEFAULT_WEB_INTERFACE_PORT
    WEB_INTERFACE = WebInterface(DEFAULT_WEB_INTERFACE_PORT)
    CLIENT = Client(WEB_INTERFACE.get_reapy_server_port())


class DistFunc:

    def __init__(self, f=None, name=None):
        if reapy.is_inside_reaper():
            self._function = f
        else:
            self._name = f.__name__ if name is None else name
            
    def __call__(self, *args, **kwargs):
        if reapy.is_inside_reaper():
            result = self._function(*args, **kwargs)
        else:
            CLIENT.send_request(self._name)
            result = CLIENT.get_result()
        return result
        
class ComposedDistFunc(DistFunc):

    def __init__(self, *functions):
        self._functions = functions
        
    def __call__(self, *args):
        if reapy
