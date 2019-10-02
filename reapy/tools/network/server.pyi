"""Define Server class."""

import reapy
from reapy.tools import json
from .socket import Socket

import socket
import traceback
import typing as ty


class Server(Socket):
    """
    Server part of the ``reapy`` dist API.

    It is instantiated inside REAPER. It receives and processes API
    call requests coming from the outside.
    """
    connections: ty.Dict[ty.Union[ty.Tuple[str, ...], str], Socket]

    def __init__(self, port: int) -> None:
        ...

    @Socket._non_blocking
    def _get_request(self, connection: Socket,
                     address: ty.Union[ty.Tuple[str, ...], str]
                     ) -> ty.Dict[str, object]:
        ...

    def _hold_connection(self, address: ty.Union[ty.Tuple[str, ...], str]
                         ) -> ty.Dict[str, ty.Optional[str]]:
        ...

    def _process_request(self, request: ty.Dict[str, object],
                         address: ty.Union[ty.Tuple[str, ...], str]
                         ) -> ty.Dict[str, ty.Any]:
        ...

    def _send_result(self, connection: Socket,
                     result: ty.Dict[str, ty.Any]) -> None:
        ...

    @Socket._non_blocking
    def accept(self, *args: ty.Any, **kwargs: ty.Any
               ) -> ty.Tuple['Socket', ty.Union[str, ty.Tuple[str, ...]]]:
        ...

    def disconnect(self, address: ty.Union[ty.Tuple[str, ...], str]) -> None:
        ...

    def get_requests(self) -> ty.Dict[str, ty.Any]:
        ...

    def process_requests(self, requests: ty.Dict[str, ty.Any]
                         ) -> ty.Dict[str, ty.Any]:
        ...

    def send_results(self, results: ty.Dict[str, ty.Any]) -> None:
        ...
