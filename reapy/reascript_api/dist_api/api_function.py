from . import _CLIENT

class APISequence:

    def __init__(self, *function_names):
        self._names = function_names
        
    def __call__(self, *args):
        _CLIENT.send_request(self._names, args)
        results = _CLIENT.get_result()
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