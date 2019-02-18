from reapy.errors import DisabledDistAPIError, UndefinedExtStateError
from reapy.tools import json
from urllib import request
from urllib.error import URLError

import reapy


class WebInterface:

    def __init__(self, port):
        self._url = "http://localhost:{}/_/".format(port)
        self.ext_state = ExtState(self)
        
    def activate_reapy_server(self):
        try:
            action_name = self.ext_state["activate_reapy_server"]
            self.perform_action(action_name)
        except UndefinedExtStateError:
            raise DisabledDistAPIError
    
    def get_reapy_server_port(self):
        try:
            port = self.ext_state["server_port"]
        except URLError:
            raise DisabledDistAPIError
        except UndefinedExtStateError:
            self.activate_reapy_server()
            port = self.get_reapy_server_port()
        return port
        
    def perform_action(self, action_id):
        url = self._url + str(action_id)
        request.urlopen(url)
        
class ExtState:

    def __init__(self, web_interface):
        self._url = web_interface._url + "{method}/EXTSTATE/reapy/{key}"

    def __getitem__(self, key):
        url = self._url.format(method="GET", key=key)
        string = request.urlopen(url).read().decode("utf-8")
        value = string.split("\t")[-1][:-1]
        if not value:
            raise UndefinedExtStateError(key)
        value = json.loads(value)
        return value
        
    def __setitem__(self, key, value):
        value = json.dumps(value)
        url = self._url + "/{value}"
        url = url.format(method="SET", key=key, value=value)
        request.urlopen(url)
