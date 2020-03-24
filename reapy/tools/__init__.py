"""Define tools such as ``inside_reaper`` and custom json module."""

import reapy
from ._inside_reaper import inside_reaper, dist_api_is_enabled
from .network.machines import connect, connect_to_default_machine, reconnect
