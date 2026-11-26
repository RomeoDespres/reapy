import time

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

    def _reconnect(self):
        """Open a new connection to the reapy server.

        Used after the connection broke, typically because REAPER was
        restarted. Goes through REAPER's web interface again, which also
        restarts the reapy server in a fresh REAPER instance.
        """
        import reapy.config
        from . import web_interface
        try:
            self.close()
        except OSError:
            pass
        Socket.__init__(self)
        interface = web_interface.WebInterface(
            reapy.config.WEB_INTERFACE_PORT, self.host
        )
        port = interface.get_reapy_server_port()
        for attempt in range(50):
            try:
                self._connect(port, self.host)
                break
            except ConnectionRefusedError:
                # A port remembered from before a restart, with no server
                # running yet: start it and give it a moment.
                if attempt == 0:
                    interface.activate_reapy_server()
                time.sleep(.1)
                Socket.__init__(self)
        else:
            raise ConnectionRefusedError(
                "reapy server not reachable on port {}".format(port)
            )
        self.port = port
        self._broken = False

    def _round_trip(self, request):
        try:
            self.send(request)
            return self._get_result()
        except OSError:
            # ConnectionError (server gone) or a socket left unconnected by a
            # failed reconnect: either way, reconnect before the next request.
            self._broken = True
            raise

    def request(self, function, input=None):
        request = {"function": function, "input": input}
        request = json.dumps(request).encode()
        if getattr(self, "_broken", False):
            # An earlier reconnect failed (e.g. REAPER was still starting).
            self._reconnect()
        try:
            result = self._round_trip(request)
        except OSError:
            # The server went away, typically because REAPER was restarted, so
            # the request was not carried out: reconnect and send it once
            # more. (If REAPER died in the middle of the call it may have run,
            # but that REAPER instance is gone with whatever it did.)
            self._reconnect()
            result = self._round_trip(request)
        if result["type"] == "result":
            return result["value"]
        elif result["type"] == "error":
            raise DistError(result["traceback"])
