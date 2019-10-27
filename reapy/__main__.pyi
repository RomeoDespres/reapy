"""Get setup infos."""

from reapy.reascripts import enable_dist_api, disable_dist_api

import os
import sys
import typing as ty


def get_config_scripts() -> ty.Tuple[str, str]:
    """
    Return paths to configuration ReaScripts.
    """
    ...


def get_python_dll() -> str:
    """
    Return path to Python DLL (if it can be found).
    """
    ...


string: str
