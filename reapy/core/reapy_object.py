class ReapyObject:

    @property
    def _args(self):
        return ()
        
    @property
    def _class_name(self):
        return "ReapyObject"
    
    @property
    def _is_defined(self):
        if hasattr(self, "id"):
            return not self.id.endswith("0x0000000000000000")
        raise NotImplementedError
        
    @property
    def _kwargs(self):
        return {}
        
    def _to_dict(self):
        return {
            "__reapy__": True,
            "class": self._class_name,
            "args": self._args,
            "kwargs": self._kwargs
        }