from warnings import warn
import reapy


class ReapyObject:
    """Base class for reapy objects."""

    def __init_subclass__(cls, subclassed=False, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.__module__.startswith('reapy'):
            if not subclassed:
                warn(reapy.errors.SubclassedWarning(str(cls)))

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
            "module": self.__module__,
            "class": self.__class__.__name__,
            "args": self._args,
            "kwargs": self._kwargs
        }


class ReapyObjectList(ReapyObject):
    """Abstract class for list of ReapyObjects."""

    pass
