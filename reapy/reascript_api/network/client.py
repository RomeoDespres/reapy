from reapy.errors import DisconnectedClientError, DistError
from reapy.tools import json
from .socket import Socket


class Client(Socket):

    def __init__(self, port):
        super(Client, self).__init__()
        self._connect(port)

    def _connect(self, port):
        super(Client, self).connect(("localhost", port))
        self.address = self.recv().decode("ascii")
        
    def _get_result(self):
        result = json.loads(self.recv().decode())
        return result
        
    def run_program(self, program, input):
        """
        Send a program to the server and return its output.
        
        Parameters
        ----------
        program : reapy.tools.Program
            Program to run.
        input : dict
            Input to the program.
            
        Returns
        -------
        result
            Program output
            
        Raises
        ------
        DistError
            When an error occurs while the server runs the program, its
            traceback is sent to the client and used to raise a 
            DistError.
        """
        program = program.to_dict()
        request = {"program": program, "input": input}
        request = json.dumps(request).encode()
        self.send(request)
        result = self._get_result()
        if result["type"] == "result":
            return result["value"]
        elif result["type"] == "error":
            raise DistError(result["traceback"])

