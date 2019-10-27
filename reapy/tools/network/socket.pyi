import socket
import typing as ty
FuncType = ty.Callable[..., ty.Any]
F = ty.TypeVar('F', bound=FuncType)
T = ty.TypeVar('T')


class Socket:
    """
    Wrapped `socket` that can send and receive data of any length.
    """
    _socket: socket.socket

    def __init__(self, s: ty.Optional['Socket'] = None) -> None:
        ...

    @staticmethod
    def _non_blocking(f: F) -> F:
        """
        Modify a socket method so that it returns `None` when time
        out is reached.
        """
        ...

    def accept(self, *args: ty.Any, **kwargs: ty.Any
               ) -> ty.Tuple['Socket', ty.Union[str, ty.Tuple[str, ...]]]:
        ...

    def bind(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...

    def close(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...

    def connect(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...

    def listen(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...

    def recv(self, timeout: float = .0001) -> bytes:
        """Receive data of arbitrary length."""
        ...

    def send(self, data: bytes) -> None:
        """Send data."""
        ...

    def settimeout(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...

    def shutdown(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        ...
