import reapy
from reapy import reascript_api as RPR
if reapy.is_inside_reaper():
    from reapy.tools.program import Program

from .socket import Socket

import json, socket

class Server(Socket):

    def __init__(self, port):
        super(Server, self).__init__()
        self.bind(("", port))
        self.listen()
        self.connections = {}
        self.settimeout(.0001)
    
    @Socket._non_blocking
    def _get_request(self, connection):
        try:
            request = connection.recv()
            request = json.loads(request.decode())
        except (ConnectionAbortedError, ConnectionResetError): # Client has disconnected
            [address] = [
                a for a, c in self.connections.items() if c is connection
            ]
            # Pretend client has nicely requested to disconnect
            code = "server.disconnect(address)"
            program = Program(code).to_dict()
            input = {"address": address, "server": self}
            request = {"program": program, "input": input}
        return request
            
    def _process_request(self, request):
        program = Program(*request["program"])
        result = {}
        request["input"].update({"RPR": RPR, "reapy": reapy})
        try:
            result["value"] = program.run(**request["input"])
            result["type"] = "result"
        except Exception as error:
            # Errors are sent back to the client instead of raised in REAPER
            # (which would cause the server to crash).
            result["value"] = error
            result["type"] = "error"
        return result
        
    def _send_result(self, connection, result):
        if result["type"] == "error":
            error = result["value"]
            result["value"] = {
                "name": error.__class__.__name__,
                "args": error.args
            }
        result = json.dumps(result).encode()
        connection.send(result)
        
    @Socket._non_blocking
    def accept(self):
        connection, address = super(Server, self).accept()
        self.connections[address] = connection
        connection.settimeout(.0001)
        connection.send("{}".format(address).encode("ascii"))
        
    def disconnect(self, address):
        connection = self.connections[address]
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
        del self.connections[address]
        
    def get_requests(self):
        requests = {}
        for address, connection in self.connections.items():
            request = self._get_request(connection)
            if request is not None:
                requests[address] = request
        return requests
        
    def process_requests(self, requests):
        results = {}
        for address, request in requests.items():
            result = self._process_request(request)
            results[address] = result
        return results
    
    def send_results(self, results):
        for address, result in results.items():
            try:
                self._send_result(self.connections[address], result)
            except KeyError:
                # Happens when the client requested to disconnect.
                # Nothing must be returned in that case.
                pass
