"""Define tools such as ``inside_reaper`` and custom json module."""

import reapy
from ._inside_reaper import inside_reaper, dist_api_is_enabled, reconnect
from .extension_dependency import depends_on_extension, depends_on_sws
