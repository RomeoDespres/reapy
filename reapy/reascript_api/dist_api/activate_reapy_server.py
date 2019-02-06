from reapy import reascript_api as RPR
from reapy.reascript_api.dist_api.network import Server, WebInterface

import os, sys

def main_loop():
    # Get new connections
    SERVER.accept()
    # Process API call requests
    requests = SERVER.get_requests()
    results = SERVER.process_requests(requests)
    SERVER.send_results(results)
    # Run main_loop again
    RPR.defer("main_loop()")

def generate_api_module():
    function_names = RPR.__all__
    filepath = os.path.join(sys.path[0], "generated_api.py")
    with open(filepath, "w") as file:
        file.write("from .api_function import APIFunction as _APIFunction\n\n")
        for name in function_names:
            file.write(
                "{name} = _APIFunction(\"RPR.{name}\")\n".format(name=name)
            )
            
def get_new_reapy_server():
    web_interface = WebInterface()
    port = web_interface.get_reapy_server_port()
    server = Server(port)
    return server

if __name__ == "__main__":
    SERVER = get_new_reapy_server()
    generate_api_module()
    main_loop()

    