from reaper_python import *

<<<<<<< HEAD
from . import call_requests
from .socket import Socket

import socket
=======
from . import _PORT, call_requests, Socket

>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89

class Server(Socket):

    def __init__(self, port):
        super(Server, self).__init__()
<<<<<<< HEAD
        self.bind(("", port))
=======
        self.bind(("", _PORT))
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
        self.listen()
        self.connections = {}
        self.settimeout(.0001)
    
    @Socket._non_blocking
    def _get_request(self, connection):
        try:
            request = connection.recv()
<<<<<<< HEAD
        except (ConnectionAbortedError, ConnectionResetError): # Client has disconnected
=======
        except ConnectionAbortedError: # Client has disconnected
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
            [address] = [
                a for a, c in self.connections.items() if c is connection
            ]
            # Pretend client has nicely requested to disconnect
<<<<<<< HEAD
            return [{"name": "DISCONNECT", "args": (address,)}]
=======
            return [{"name": "self.disconnect", "args": (address,)}]
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
        request = call_requests.decode_request(request)
        return request
            
    def _process_request(self, request):
<<<<<<< HEAD
        result = [None]*len(request)
        for i, r in enumerate(request):
            try:
                if r["name"] == "DISCONNECT":
                    self.disconnect(r["args"][0])
                else:
                    result[i] = eval(r["name"])(*r["args"])
=======
        result = [0]*len(request)
        for i, r in enumerate(request):
            try:
                result[i] = eval(r["name"])(*r["args"])
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
            except Exception as error:
                result[i] = error
        return result
        
    def _send_result(self, connection, result):
        result = call_requests.encode_result(result)
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
