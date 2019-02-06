<<<<<<< HEAD
import reapy

from .network import Client, WebInterface

if reapy.is_inside_reaper():
    from reaper_python import *
else:
    _CLIENT = Client(WebInterface().get_reapy_server_port())
=======
from . import _CLIENT
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89

class APISequence:

    def __init__(self, *function_names):
        self._names = function_names
        
    def __call__(self, *args):
<<<<<<< HEAD
        if reapy.is_inside_reaper():
            results = [eval(n)(*a) for n, a in zip(self._names, args)]
        else:
            _CLIENT.send_request(self._names, args)
            results = _CLIENT.get_result()
=======
        _CLIENT.send_request(self._names, args)
        results = _CLIENT.get_result()
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
        return results
    
    def __repr__(self):
        return "API sequence {}".format(self._names)
        
class APIFunction(APISequence):

    def __call__(self, *args):
        results = super(APIFunction, self).__call__(args)
        return results[0]
        
    def __repr__(self):
        repr = "API function {}".format(self._names[0])
        return repr