from reapy.errors import DisconnectedClientError, DistError
from reapy.tools import json
from .socket import Socket


class Client(Socket):

    def __init__(self, port, host="localhost"):
        super().__init__()
        self._connect(port, host)
        self.port, self.host = port, host

    def _connect(self, port, host):
        super().connect((host, port))
        self.address = self.recv(timeout=None).decode("ascii")

    def _get_result(self):
        s = self.recv(timeout=None).decode()
        return json.loads(s)

    def request(self, function, input=None):
        request = {"function": function, "input": input}
        request = json.dumps(request).encode()
        self.send(request)
        result = self._get_result()
        if result["type"] == "result":
            return result["value"]
        elif result["type"] == "error":
            raise DistError(result["traceback"])
