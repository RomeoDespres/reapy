from .network.client import Client

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