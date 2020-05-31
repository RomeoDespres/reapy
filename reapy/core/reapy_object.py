import reapy
import reapy.reascript_api as RPR
from functools import partial


class ReapyMetaclass(type):

    @property
    def _reapy_parent(self):
        """Return first reapy parent class."""
        for candidate in self.__mro__:
            if candidate.__module__.startswith('reapy.'):
                return candidate


class ReapyObject(metaclass=ReapyMetaclass):
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

    def _get_pointer_and_name(self):
        name, pointer = self.id.split(')')
        return int(pointer, base=16), name[1:]

    @property
    def _is_defined(self):
        if hasattr(self, "id"):
            return not self.id.endswith("0x0000000000000000")
        raise NotImplementedError

    @property
    def _kwargs(self):
        return {}

    @property
    def _state(self):
        return None

    @_state.setter
    def _state(self, state):
        if state is None:
            return
        self.__dict__.update(state)

    def _to_dict(self):
        return {
            "__reapy__": True,
            "module": self.__class__._reapy_parent.__module__,
            "class": self.__class__._reapy_parent.__name__,
            "args": self._args,
            "kwargs": self._kwargs,
            "state": self._state
        }

    @reapy.inside_reaper()
    def map(self, method_name, iterables, defaults=None):
        """
        Perform object method among iterables inside reaper.

        Note
        ----
        Opposite to `inside_reaper`, which saves on deferred executions,
        map saves on socket connections, so, basically, if you have complex
        code needs to be performed at one deferred call — use `inside_reaper`,
        if large amount of data has to be proceed within particular method —
        use `object.map()`.

        Parameters
        ----------
        method_name : str
            name of the object method (self)
        iterables : Dict[str, List[jsonable]]
            str is argument name, List for mapping
        defaults : Dict[str, jsonable]
            partial arguments, that won't be changed though iteration

        Returns
        -------
        List[<method result>]

        Example
        -------
        import reapy as rpr
        take = rpr.Project().selected_items[0].active_take

        @rpr.inside_reaper()
        def test():
            for i in [6.0] * 1000000:
                take.time_to_ppq(6.0)


        def test_map():
            take.map('time_to_ppq', iterables={'time': [6.0] * 1000000})


        test()      # runs 140s
        test_map()  # runs 12s as from outside as from inside
        """
        result = []
        if defaults:
            part_func = partial(getattr(self, method_name), **defaults)
        else:
            part_func = getattr(self, method_name)

        for values in zip(*iterables.values()):
            rest = {k: v for k, v in zip(iterables.keys(), values)}
            result.append(part_func(**rest))
        return result


class ReapyObjectList(ReapyObject):
    """Abstract class for list of ReapyObjects."""

    pass
