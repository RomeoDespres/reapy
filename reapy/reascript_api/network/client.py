from .socket import Socket
from .errors import DisconnectedClientError

import json

class Client(Socket):

    def __init__(self, port):
        super(Client, self).__init__()
        self.connect(port)

    def connect(self, port):
        super(Client, self).connect(("localhost", port))
        self.address = self.recv().decode("ascii")
        
    def run_program(self, program, input):
        program = program.to_dict()
        request = {"program": program, "input": input}
        request = json.dumps(request).encode()
        self.send(request)
        result = self.get_result()
        return result
    
    def get_result(self):
        result = json.loads(self.recv().decode())
        if result["type"] == "error":
            error = result["value"]
            try:
                raise eval(error["name"])(*error["args"])
            except NameError as e:
                if error["name"] == "NameError":
                    raise e
                raise Exception(error["name"], *error["args"])
        return result["value"]

