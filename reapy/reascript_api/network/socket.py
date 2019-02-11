import socket

class Socket:

    """
    Wrapped `socket` that can send and receive data of any length.
    """

    def __init__(self, s=None):
        self._socket = socket.socket() if s is None else s
    
    @staticmethod
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
        
    def accept(self, *args, **kwargs):
        connection, address = self._socket.accept(*args, **kwargs)
        connection = Socket(connection)
        return connection, address
        
    def bind(self, *args, **kwargs):
        return self._socket.bind(*args, **kwargs)
        
    def close(self, *args, **kwargs):
        return self._socket.close(*args, **kwargs)
        
    def connect(self, *args, **kwargs):
        return self._socket.connect(*args, **kwargs)
        
    def listen(self, *args, **kwargs):
        return self._socket.listen(*args, **kwargs)
        
    def recv(self):
        """
        Receive data of arbitrary length.
        """
        # First get data length
        length = self._socket.recv(8)
        length = int.from_bytes(length, "little")
        if length == 0:
            raise ConnectionAbortedError
        # Then receive data (split it into smaller bits if too big)
        data = b""
        max_size = 2**32
        for _ in range(length // max_size):
            data += self._socket.recv(max_size)
        data += self._socket.recv(length % max_size)
        return data
    
    def send(self, data):
        """
        Send data.
        """
        # First send data length
        length = len(data).to_bytes(8, "little")
        self._socket.send(length)
        # Then send data
        self._socket.send(data)
        
    def settimeout(self, *args, **kwargs):
        return self._socket.settimeout(*args, **kwargs)
        
    def shutdown(self, *args, **kwargs):
        return self._socket.shutdown(*args, **kwargs)