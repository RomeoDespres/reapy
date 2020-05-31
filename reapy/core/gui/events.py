import typing as ty
import typing_extensions as te

import reapy
from reapy.core import ReapyObject
from .singleton import Singleton, UUID, SingletonMeta


class Event(ReapyObject):
    pass


class EventQueueItem(te.TypedDict):
    event: Event
    clients: ty.List[UUID]


class EventClientMeta(SingletonMeta):

    def __call__(  # type:ignore
        cls, *args, uuid: ty.Optional[UUID] = None, **kwargs
    ) -> 'EventClient':
        if uuid in cls._uuid_index:
            return super().__call__(*args, uuid=uuid, **kwargs)  # type:ignore
        obj = super().__call__(*args, uuid=uuid, **kwargs)
        obj.event_handler.register_client(obj)  # type:ignore
        return obj  # type:ignore


class EventClient(Singleton, metaclass=EventClientMeta):
    event_handler: 'EventHandler'

    def __init__(self, event_handler: 'EventHandler') -> None:
        self.event_handler = event_handler

    def on_event(self, event: Event) -> None:
        """Handle general event.

        Note
        ----
        Usually, this method should filter events interesting to the
        particular class, then passthrough other events with or without
        filtered event to the super().on_event().

        Parameters
        ----------
        event : Event
        """


class EventHandler(Singleton):
    """Suppose to handle event loop as from outside, as from inside.

    Usage
    -----
    Event Handler makes possible to run event loop from outside.
    So, only one EventHandler() on loop has to be used.
    * create Handler and assign to event loop provider (currently — TopLevel)
    * ensure provider has the same EventHandler as from outside as from inside
    * fire events from the inside or outside loop
    * fire queue every otside frame (deferred call)
    * PROFIT!

    Note
    ----
    When running outside one frame may consists of multiple events, for example:
        frame A
        on_key_char(time=17490.50636416, char=a, mod=<vVirtKey.1: 1>)
        frame B
        on_key_char(time=17490.529582476, char=s, mod=<vVirtKey.1: 1>)
        on_key_char(time=17490.574602799, char=d, mod=<vVirtKey.1: 1>)
        frame C
        on_key_char(time=17490.597725631, char=f, mod=<vVirtKey.1: 1>)

    Attributes
    ----------
    buffered : bool
        whether event loop runs from outside (True) of inside
    """

    def __init__(self, buffered: ty.Optional[bool] = None) -> None:
        """Create EventHandler object

        Parameters
        ----------
        buffered : Optional[bool], do not use.
            used internally and assigned automatically.
        """
        self.buffered = (
            buffered if buffered is not None else not reapy.is_inside_reaper()
        )
        self.clients: ty.Dict[UUID, EventClient] = {}
        self._queue: ty.List[EventQueueItem] = []

    @property
    def _args(self) -> ty.Tuple[ty.Optional[bool]]:
        return (self.buffered, )

    @reapy.inside_reaper()
    def get_queue(self) -> ty.List[EventQueueItem]:
        """Get queued events.

        Returns
        -------
        List[EventQueueItem]
        """
        return self._queue

    @reapy.inside_reaper()
    def clear_queue(self) -> None:
        self._queue.clear()

    def fire_event(self, event: Event, clients: ty.List[EventClient]) -> None:
        """Put event to queue or launch corresponding callbacks on clients.

        Parameters
        ----------
        event : Event
        clients : List[EventClient]
        """
        if self.buffered and reapy.is_inside_reaper():
            return self.event_to_queue(event, clients)
        for client in clients:
            client.on_event(event)

    def fire_queue(self) -> None:
        """Fire all queued events."""
        queue = self.get_queue()
        for item in queue:
            self.fire_event(
                item["event"],
                [self.clients[client] for client in item["clients"]]
            )
        self.clear_queue()

    def event_to_queue(
        self, event: Event, clients: ty.List[EventClient]
    ) -> None:
        """Put event to queue for being fired from outside.

        Note
        ----
        There should not be use-cases other than internal.
        But I'll leave it public for being more verbose.

        Parameters
        ----------
        event : Event
        clients : List[EventClient]
        """
        self._queue.append(
            EventQueueItem(event=event, clients=[cl.uuid for cl in clients])
        )

    def register_client(self, client: EventClient) -> None:
        """Let EventHandler recognize client later.

        Parameters
        ----------
        client : EventClient
        """
        self.clients[client.uuid] = client
