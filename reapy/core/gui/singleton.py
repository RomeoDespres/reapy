import typing as ty
from uuid import uuid4
from reapy.core.reapy_object import ReapyMetaclass, ReapyObject

UUID = ty.NewType('UUID', str)


class SingletonMeta(ReapyMetaclass):

    def __call__(
        cls, *args, uuid: ty.Optional[UUID] = None, **kwargs
    ) -> 'Singleton':
        if uuid is None:
            uuid = str(uuid4())  # type:ignore
        if uuid in cls._uuid_index:
            return cls._uuid_index[uuid]
        obj = super().__call__(*args, **kwargs)
        obj.uuid = uuid
        cls._uuid_index[uuid] = obj
        return obj


class Singleton(ReapyObject, metaclass=SingletonMeta):
    """Reapy Singleton.
    Guarantees, that object outside Reaper refers always
    to the same object inside.

    Note
    ----
    if _kwargs property is being overriden, get the dict from the super()
    at first, then update with your kwargs:
        `return super()._kwargs.update(<my_kwargs>)`

    Attributes
    ----------
    uuid : UUID
        as id, just uuid
    """

    _uuid_index: ty.Dict[UUID, 'Singleton'] = {}
    uuid: UUID

    @property
    def _kwargs(self) -> ty.Dict[str, object]:
        d = super()._kwargs
        d.update({'uuid': self.uuid})
        return d
