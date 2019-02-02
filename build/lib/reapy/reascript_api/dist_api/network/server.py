from . import _PORT, call_requests 

import socket


def _non_blocking(f):
    """
    Modify a socket method so that it returns `None` when time out is reached.
    """
    def g(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except socket.timeout:
            pass
    return g


class Server(socket.socket):

    def __init__(self):
        super(Server, self).__init__()
        self._buffer_size = 4096
        self.bind(("", _PORT))
        self.listen()
        self.connections = {}
        self.settimeout(.0001)
        
    @_non_blocking
    def _get_request(self, connection):
        request = connection.recv(self._buffer_size)
        if not request: # Means client has disconnected.
            [address] = [
                a for a, c in self.connections.items() if c is connection
            ]
            return "SERVER.disconnect", (address,)
        else: # Process request
            return call_requests.decode_request(request)
            
    def _send_error(self, connection, error):
        error = call_requests.encode_error(error)
        connection.send(error)
        
    def _send_result(self, connection, result):
        result = call_requests.encode_result(result)
        connection.send(result)
        
    @_non_blocking
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
    
    def send_errors(self, errors):
        for address, error in errors.items():
            self._send_error(self.connections[address], error)
    
    def send_results(self, results):
        for address, result in results.items():
            try:
                self._send_result(self.connections[address], result)
            except KeyError:
                # Happens when the client requested to disconnect.
                # Nothing must be returned in that case.
                pass
