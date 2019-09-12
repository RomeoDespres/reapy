"""
Activate ``reapy`` server.

Running this ReaScript from inside REAPER sets the ``reapy`` server
that receives and executes API calls requests from outside. It will
automatically be run when importing ``reapy`` from outside, if it is
enabled.
"""

import reapy

import os
import site

from reapy.tools.network import Server


def run_main_loop():
    # Get new connections
    SERVER.accept()
    # Process API call requests
    requests = SERVER.get_requests()
    results = SERVER.process_requests(requests)
    SERVER.send_results(results)
    # Run main_loop again
    reapy.defer(run_main_loop)


def get_new_reapy_server():
    server_port = reapy.config.REAPY_SERVER_PORT
    reapy.set_ext_state("reapy", "server_port", server_port)
    server = Server(server_port)
    return server


if __name__ == "__main__":
    SERVER = get_new_reapy_server()
    run_main_loop()
    reapy.at_exit(reapy.delete_ext_state, "reapy", "server_port")
