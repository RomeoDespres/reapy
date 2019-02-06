from reaper_python import *
from reaper_python import _ft # dict with API function names as keys

from network.server import Server

import json, os, sys

def main_loop():
    # Get new connections
    SERVER.accept()
    # Process API call requests
    requests = SERVER.get_requests()
    results = {}
    errors = {}
    for address, request in requests.items():
        function_name, args = request
        try:
            results[address] = eval(function_name)(*args)
        except Exception as e:
            errors[address] = e
    SERVER.send_results(results)
    SERVER.send_errors(errors)
    # Run main_loop again
    RPR_defer("main_loop()")

def generate_api_module():
    function_names = map(lambda x: "RPR_" + x, _ft.keys())
    filepath = os.path.join(sys.path[0], "generated_api.py")
    with open(filepath, "w") as file:
        file.write("from . import _api_function\n\n")
        for function_name in function_names:
            file.write("@_api_function\n")
            file.write("def {}():\n    pass\n\n".format(function_name))

if __name__ == "__main__":
    SERVER = Server()
    generate_api_module()
    main_loop()
