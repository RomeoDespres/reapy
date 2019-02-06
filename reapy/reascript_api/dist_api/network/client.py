<<<<<<< HEAD
from . import call_requests
from .socket import Socket
from .errors import DisconnectedClientError
=======
from . import _PORT, call_requests, Socket
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89


class Client(Socket):

    def __init__(self, port):
        super(Client, self).__init__()
<<<<<<< HEAD
        self.connect(port)

    def connect(self, port):
        super(Client, self).connect(("localhost", port))
=======
        self.connect()

    def connect(self):
        super(Client, self).connect(("localhost", _PORT))
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
        self.address = self.recv().decode("ascii")
        self.is_connected = True
        
    def disconnect(self):
<<<<<<< HEAD
        self.send_request("DISCONNECT", (self.address,))
=======
        self.send_request("self.disconnect", (self.address,))
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
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
<<<<<<< HEAD
=======


class DisconnectedError(Exception):

    def __init__(self):
        message = "Client disonnected. Call self.connect to reconnect."
        super(DisconnectedError, self).__init__(message)
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
