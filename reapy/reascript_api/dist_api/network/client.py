from . import call_requests
from .socket import Socket
from .errors import DisconnectedClientError


class Client(Socket):

    def __init__(self, port):
        super(Client, self).__init__()
        self.connect(port)

    def connect(self, port):
        super(Client, self).connect(("localhost", port))
        self.address = self.recv().decode("ascii")
        self.is_connected = True
        
    def disconnect(self):
        self.send_request("DISCONNECT", (self.address,))
        self.is_connected = False
    
    def get_result(self):
        if not self.is_connected:
            raise DisconnectedError
        result = self.recv()
        result = call_requests.decode_result(result)
        return result
    
    def send_request(self, function_name, args=()):
        if not self.is_connected:
            raise DisconnectedClientError
        request = call_requests.encode_request(function_name, args)
        self.send(request)
