import typing as ty
import typing_extensions as te

import atexit
from enum import Enum, auto

import reapy
from reapy.core import ReapyObject
from .singleton import Singleton, UUID, SingletonMeta
from . import JS


class EventTarget(Enum):
    """Used to specify event targets relatively for EventClient."""
    everyone = auto()
    parent = auto()
    childs = auto()
    self_ = auto()


class Event(ReapyObject):
    pass


class EvFrame(Event):
    """Fired every loop frame."""


class EvStart(Event):
    """Fired on mainloop start."""


class EvExit(Event):
    """Fired on mainloop exit."""


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


ListOfEventOrUUID = ty.Union[ty.List['EventClient'], ty.List[UUID]]


class EventHandler(Singleton):
    """Suppose to handle event loop as from outside, as from inside.

    Usage
    -----
    Event Handler makes possible to run event loop from outside.
    So, only one EventHandler() on loop has to be used.
    * create Handler and assign to event loop provider (currently — TopLevel)
    * ensure provider has the same EventHandler as from outside as from inside
    * fire events from the inside or outside loop
    * fire queue every outside frame (deferred call)
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

    def fire_event(
        self, event: Event, clients: ty.Optional[ListOfEventOrUUID]
    ) -> None:
        """Put event to queue or launch corresponding callbacks on clients.

        Parameters
        ----------
        event : Event
        clients : Optional[List[EventClient]]
            If None — fires to every registered client.
        """
        if clients is None:
            clients = list(self.clients.values())
        if self.buffered and reapy.is_inside_reaper():
            return self.event_to_queue(event, clients)
        for client in clients:
            if not isinstance(client, EventClient):
                client = self.clients[client]
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

    def event_to_queue(self, event: Event, clients: ListOfEventOrUUID) -> None:
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
            EventQueueItem(
                event=event,
                clients=[
                    cl.uuid if isinstance(cl, EventClient) else cl
                    for cl in clients
                ]
            )
        )

    @reapy.inside_reaper()
    def _register_client_inside(self, client: 'EventClient') -> None:
        self.register_client(client)

    def register_client(self, client: 'EventClient') -> None:
        """Let EventHandler recognize client later.

        Parameters
        ----------
        client : EventClient
        """
        self.clients[client.uuid] = client
        if not reapy.is_inside_reaper():
            self._register_client_inside(client)

    @reapy.inside_reaper()
    def _remove_client_inside(self, client: 'EventClient') -> None:
        self.remove_client(client)

    def remove_client(self, client: 'EventClient') -> None:
        """Let EventHandler recognize client later.

        Parameters
        ----------
        client : EventClient
        """
        del self.clients[client.uuid]
        if not reapy.is_inside_reaper():
            self._remove_client_inside(client)


class EventClient(Singleton, metaclass=EventClientMeta):
    event_handler: 'EventHandler'
    parent: ty.Optional['EventClient']
    childs: ty.Dict[UUID, 'EventClient']

    def __init__(self, event_handler: 'EventHandler') -> None:
        self.event_handler = event_handler
        self.parent = None
        self.childs = {}

    @property
    def _state(self) -> ty.Dict[str, object]:
        return {
            **super()._state, 'parent': self.parent,
            'childs': self.childs,
            'event_handler': self.event_handler
        }

    def on_event(self, event: Event) -> None:
        """Handle general event.

        Note
        ----
        Usually, this method should filter events interesting to the
        particular class, then pass through other events with or without
        filtered event to the super().on_event().

        Parameters
        ----------
        event : Event
        """
        if isinstance(event, EvFrame):
            return self.run()
        if isinstance(event, EvExit):
            return self.cleanup()
        if isinstance(event, EvStart):
            return self.setup()
        return None

    def fire_event(
        self,
        event: Event,
        clients: ty.Union[ty.List['EventClient'],
                          EventTarget] = EventTarget.childs
    ) -> None:
        if isinstance(clients, ty.Iterable):
            return self.event_handler.fire_event(event, clients)
        if clients == EventTarget.everyone:
            return self.event_handler.fire_event(event, None)
        if clients == EventTarget.childs:
            return self.event_handler.fire_event(
                event, list(self.childs.values())
            )
        if clients == EventTarget.self_:
            return self.event_handler.fire_event(event, [self])
        if clients == EventTarget.parent:
            if self.parent is None:
                raise RuntimeError(
                    'object {} does not have parent'.format(self)
                )
            return self.event_handler.fire_event(event, None)

    def add_child(self, child: 'EventClient') -> None:
        child.event_handler = self.event_handler
        child.parent = self
        self.event_handler.register_client(child)
        self.childs.update({child.uuid: child})
        if self.is_running():
            child.setup()

    def delete_child(
        self,
        child: ty.Union['EventClient', UUID],
        finalize: bool = True
    ) -> None:
        child = child if isinstance(child, EventClient) else self.childs[child]
        if finalize:
            child.cleanup()
        del self.childs[child.uuid]

    @reapy.inside_reaper()
    def is_running(self) -> bool:
        """Whether event loop is running."""
        if self.parent is None:
            return False
        return self.parent.is_running()

    def setup(self) -> None:
        """User-method to be called at first mainloop iteration.

        Note
        ----
        super().setup() has to be used at the end of overloaded method.
        """
        # for child in self.childs.values():
        #     child.setup()

    def _loop_frame(self) -> None:
        """Reapy internal method to be called on every frame."""

    def run(self) -> None:
        """User-method to be called every loop frame.

        Note
        ----
        super().run() has to be used at the end of overloaded method.
        """
        for child in self.childs.values():
            child.run()

    def cleanup(self) -> None:
        """User-method to be called at exit.

        Note
        ----
        super().cleanup() has to be used at the end of overloaded method.
        """
        for child in self.childs.values():
            child.cleanup()
        self.event_handler.remove_client(self)


class EventLoop(EventClient):
    """
    Pure realization of event loop.


    Methods to be overridden
    -----------------------
    def should_exit(self) -> bool: ...  True if loop has to be killed
    def _launch(self) -> None: ...       as setup
    def _loop_frame(self) -> None: ...   the same as run()
    def _kill(self) -> None: ...         as cleanup
    """

    def __init__(self) -> None:
        super().__init__(EventHandler())
        self._running = False

    @property
    def _state(self) -> ty.Dict[str, object]:
        return {**super()._state, "_running": self._running}

    @reapy.inside_reaper()
    def is_running(self) -> bool:
        return self._running

    def mainloop(self) -> None:
        """Launch mainloop."""
        self.start()
        if not reapy.is_inside_reaper():
            atexit.register(self._at_exit)
            while self.is_running:
                with reapy.inside_reaper():
                    self.event_handler.fire_queue()

    @reapy.inside_reaper()
    def start(self) -> None:
        """Launch event loop.

        Not the best way to make event loop.
        Runs internally, but, theoretically, can be used.
        """
        self._running = True
        self._launch()
        reapy.at_exit(self._at_exit)
        self.fire_event(EvStart(), EventTarget.everyone)
        self._loop()

    def _launch(self) -> None:
        """Reapy internal method to be called on start."""

    @reapy.inside_reaper()
    def _loop(self) -> None:
        if self.should_exit() is True is self.is_running():
            self._kill()
            return
        try:
            self._loop_frame()
            self.fire_event(EvFrame(), EventTarget.everyone)
            reapy.defer(self._loop)
        except KeyboardInterrupt as e:
            self._kill()
            raise e

    def should_exit(self) -> bool:
        """Whether event loop should be killed."""
        return False

    def _loop_frame(self) -> None:
        """Reapy internal method to be called on every frame."""
        for child in self.childs.values():
            child._loop_frame()

    @reapy.inside_reaper()
    def _at_exit(self) -> None:
        self.fire_event(EvExit(), EventTarget.everyone)
        if not self.is_running():
            return
        self._kill()

    def _kill(self) -> None:
        """Reapy internal method to be called for cleanup."""
