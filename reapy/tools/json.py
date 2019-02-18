import json


class ReapyEncoder(json.JSONEncoder):
    
    def default(self, x):
        if any(isinstance(x, c) for c in _CLASSES.values()):
            return x._to_dict()
        return json.JSONEncoder.default(self, x)
        
def loads(s):
    return json.loads(s, object_hook=object_hook)

def dumps(x):
    return json.dumps(x, cls=ReapyEncoder)

def object_hook(x):
    if "__reapy__" not in x:
        return x
    core = importlib.import_module("reapy.core")
    reapy_class = dir(core)[x["class"]]
    return reapy_class(*x["args"], **x["kwargs"])


