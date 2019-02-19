class ReapyObject:

    """Base class for reapy objects."""
    
    _class_name = "ReapyObject"

    def __repr__(self):
        def to_str(x):
            if isinstance(x, str):
                return "\"{}\"".format(x)
            return str(x)
        args = ", ".join(map(to_str, self._args))
        kwargs = ", ".join(
            ("{}={}".format(k, to_str(v)) for k, v in self._kwargs.items())
        )
        if args and kwargs:
            brackets = ", ".join((args, kwargs))
        else:
            brackets = args if args else kwargs
        rep = "{}({})".format(self._class_name, brackets)
        return rep

    @property
    def _args(self):
        return ()
    
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