import reapy
import reapy.core

import inspect, os, pandas as pd

# Helper functions
def double_quoted(s):
    return repr(s).replace("'", '"')
    
def get_reapy_module(s):
    parts = s.split(".")
    if s[0].lower() != s[0]:
        parts = parts[:-1]
    o = reapy
    for a in parts:
        o = getattr(o, a)
    module = inspect.getmodule(o)
    return module
    
def reapy_link(s):
    if s in ("TODO", "DEPRECATED"):
        return s
    module = get_reapy_module(s)
    page = module.__package__ + ".html"
    anchor = ".".join((module.__name__, s))
    url = page + "#" + anchor
    return rst_link(s, url)
    
def reascript_link(s):
    page = "https://www.reaper.fm/sdk/reascript/reascripthelp.html"
    anchor = s
    url = page + "#" + anchor
    return rst_link(s, url)
    
def rst_link(s, url):
    return "`{} <{}>`_".format(s, url)

# Load api.csv
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "docs", "api.csv"))

# Open output file
output_path = os.path.join(
    os.path.dirname(__file__), "docs", "source", "api_table.rst"
)
f = open(output_path, "w")

# Write header
f.write(
"""
Translation table
=================

.. csv-table::
    :header: "ReaScript API function", "``reapy`` API function"

"""
)

# Write contents
for reascript_name, reapy_name in df.values:
    f.write("".join((
        "\t",
        double_quoted(reascript_link(reascript_name)),
        ",",
        double_quoted("; ".join(map(reapy_link, reapy_name.split(";")))),
        "\n"
    )))
    
f.close()