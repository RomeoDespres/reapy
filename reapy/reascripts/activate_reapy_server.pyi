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

SERVER: Server


def run_main_loop() -> None:
    ...


def get_new_reapy_server() -> Server:
    ...
