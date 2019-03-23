from reapy.tools import Program


class ReapyObject:

    """Base class for reapy objects."""

    def __eq__(self, other):
        return repr(self) == repr(other)

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
        rep = "{}({})".format(self.__class__.__name__, brackets)
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
            "class": self.__class__.__name__,
            "args": self._args,
            "kwargs": self._kwargs
        }


class ReapyObjectList(ReapyObject):

    """Abstract class for list of ReapyObjects."""

    def __iter__(self):
        code = """
        elements = [ro_list[i] for i in range(len(ro_list))]
        """
        elements, = Program(code, "elements").run(ro_list=self)
        for element in elements:
            yield element

