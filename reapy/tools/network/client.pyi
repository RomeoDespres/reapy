from reapy.errors import DisconnectedClientError, DistError
from reapy.tools import json
from .socket import Socket
import typing as ty


class Client(Socket):
    address: str

    def __init__(self, port: int) -> None:
        ...

    def _connect(self, port: int) -> None:
        ...

    def _get_result(self) -> ty.Any:
        ...

    def request(self,
                function: ty.Callable[..., ty.Any],
                input: ty.Optional[object] = None) -> ty.Any:
        ...
