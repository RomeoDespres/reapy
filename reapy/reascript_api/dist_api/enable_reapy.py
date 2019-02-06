from reaper_python import *
from reaper_python import _ft # dict with API function names as keys

from network import Server, WebInterface

import os, sys

def main_loop():
    # Get new connections
    SERVER.accept()
    # Process API call requests
    requests = SERVER.get_requests()
    results = SERVER.process_requests(requests)
    SERVER.send_results(results)
    # Run main_loop again
    RPR_defer("main_loop()")

def generate_api_module():
    filepath = os.path.join(sys.path[0], "generated_api.py")
    with open(filepath, "w") as file:
<<<<<<< HEAD
        file.write("from .api_function import APIFunction as _APIFunction\n\n")
        for name in _ft:
            file.write(
                "{name} = _APIFunction(\"RPR_{name}\")\n".format(name=name)
=======
        file.write("from .api_function import APIFunction\n\n")
        for name in _ft:
            file.write(
                "{name} = APIFunction(\"RPR_{name}\")\n".format(name=name)
>>>>>>> 2e6af04aaab5355e80ef3da42726ae9008b86f89
            )

if __name__ == "__main__":
    SERVER = Server()
    generate_api_module()
    main_loop()
