from . import _CLIENT

class APIFunction:

    def __init__(self, *function_names):
        self._names = function_names
        
    def __call__(self, *args):
        if len(self.names) == 1:
            args = (args,)
        _CLIENT.send_request(self.names, args)
        results = _CLIENT.get_result()
        if len(results) == 1:
            return results[0]
        else:
            return results
    
    def __repr__(self):
        if len(self.names) == 1:
            return "API function {}".format(self.names[0])
        return "API functions {}".format(self.names)
        
