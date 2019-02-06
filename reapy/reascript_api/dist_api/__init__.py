import reapy

<<<<<<< HEAD
if not reapy.is_inside_reaper():
    from .generated_api import *
=======
_CLIENT = Client()

def _api_function(f):
    def g(*args):
        _CLIENT.send_request(f.__name__, args)
        return _CLIENT.get_result()
    return g

try:
    from .generated_api import *
except ModuleNotFoundError as error:
    args = (error.args[0] + "\nHave you enabled reapy from REAPER?",) + error.args[1:]
    error.args = args
    raise ModuleNotFoundError(*args)
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
