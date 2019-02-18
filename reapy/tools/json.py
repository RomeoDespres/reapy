import importlib, json


class ReapyEncoder(json.JSONEncoder):
    
    def default(self, x):
        core = importlib.import_module("reapy.core")
        if any(isinstance(x, getattr(core, c)) for c in core.__all__):
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
    reapy_class = getattr(core, x["class"])
    return reapy_class(*x["args"], **x["kwargs"])


