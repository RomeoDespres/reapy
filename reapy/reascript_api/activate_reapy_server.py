import reapy
from reapy import reascript_api as RPR
from reapy.config import config
from reapy.reascript_api.network import Server

import os, sys, tempfile

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
    function_names = RPR.__all__
    filepath = os.path.join(tempfile.gettempdir(), "reapy_generated_api.py")
    with open(filepath, "w") as file:
        lines = [
            "from reapy.tools import Program",
            "",
            "__all__ = ["
        ]
        lines += ["    \"{}\",".format(name) for name in function_names]
        lines.append("]\n\n")
        file.write("\n".join(lines))
        for name in function_names:
            file.write(
                "{name} = Program.from_function(\"RPR.{name}\")\n".format(name=name)
            )
            
def get_new_reapy_server():
    server_port = config.REAPY_SERVER_PORT
    reapy.set_ext_state("reapy", "server_port", server_port)
    server = Server(server_port)
    return server

if __name__ == "__main__":
    SERVER = get_new_reapy_server()
    generate_api_module()
    main_loop()
    RPR_atexit("""reapy.delete_ext_state("reapy", "server_port")""")

    