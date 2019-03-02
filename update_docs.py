"""
Build ``docs/source/api_table.rst`` from ``docs/api.json``.
"""

import reapy
import reapy.core

from collections import defaultdict
import inspect
import json
import os
from sphinx.cmd.build import build_main as sphinx_build_cmd


HEADER = """
Translation Table
=================

On this page you can find the list of all ReaScript API functions with their ``reapy`` counterparts (when they exist).

Categories are based on Mespotine's `ReaScript documentation <https://mespotin.uber.space/Mespotine/Ultraschall/Reaper_Api_Documentation.html>`_.

.. contents:: Categories
    :local:
    :depth: 2


"""


def build_api_table():
    api_infos = load_api_infos()
    groups = get_groups(api_infos)
    output_path = get_output_path()
    f = open(output_path, "w")
    f.write(HEADER)
    for group_name, group in sorted(groups.items()):
        f.write(get_group_string(group_name, group))
    f.close()


def double_quoted(s):
    return repr(s).replace("'", '"')


def load_api_infos():
    path = get_input_path()
    with open(path) as f:
        return json.load(f)


def get_changelog_links():
    api = load_api_infos()
    names = set(
        n for info in api.values() for n in info["reapy"] if n != "DEPRECATED"
    )
    links = sorted([reapy_link(n, type="md") + "\n" for n in names])
    return links


def get_group_contents(group):
    string = (
        ".. csv-table::\n"
        "\t:header: \"ReaScript API function\", \"reapy API function\""
        "\n\n"
    )
    for reascript_name, infos in group.items():
        reapy_names = infos["reapy"]
        string += "\t{},{}\n".format(
            double_quoted(reascript_link(reascript_name)),
            double_quoted("; ".join(map(reapy_link, reapy_names)))
        )
    return string


def get_group_string(group_name, group):
    contents = get_group_contents(group)
    return "{}\n{}\n\n{}\n\n".format(
        group_name, "-"*len(group_name), contents
    )


def get_groups(infos):
    groups = defaultdict(dict)
    for name, info in infos.items():
        groups[info["group"]][name] = info
    return groups


def get_input_path():
    path = os.path.join(os.path.dirname(__file__), "docs", "api.json")
    return path


def get_output_path():
    output_path = os.path.join(
        os.path.dirname(__file__), "docs", "source", "api_table.rst"
    )
    return output_path


def get_reapy_module(s):
    parts = s.split(".")
    if s[0].lower() != s[0]:
        parts = parts[:-1]
    o = reapy
    for a in parts:
        o = getattr(o, a)
    module = inspect.getmodule(o)
    return module


def markdown_link(s, url):
    return "[{}]: {}".format(s, url)


def reapy_link(s, type="rst"):
    if s == "DEPRECATED":
        return s
    if s in ("defer", "at_exit"):
        url = "reapy.core.reaper.html#reapy.core.reaper.defer.{}".format(s)
    else:
        if s[0].lower() != s[0]:
            page = "reapy.core.html"
            anchor = "reapy.core." + s
        else:
            page = "reapy.core.reaper.html"
            anchor = "reapy.core.reaper."
            if "." in s:
                anchor += s
            else:
                anchor += "reaper." + s
        url = page + "#" + anchor
    if type == "rst":
        return rst_link(s, url)
    else:
        return markdown_link("`{}`".format(s), url)


def reascript_link(s):
    page = "https://www.reaper.fm/sdk/reascript/reascripthelp.html"
    anchor = s
    if s in ("defer", "atexit"):
        anchor = "python_" + anchor
    url = page + "#" + anchor
    return rst_link(s, url)


def rst_link(s, url):
    return "`{} <{}>`_".format(s, url)


def sphinx_build():
    root = os.path.dirname(__file__)
    source = os.path.join(root, "docs", "source")
    build = os.path.join(root, "docs", "build", "html")
    sphinx_build_cmd([source, build])


def update_changelog():
    changelog_path = os.path.join(os.path.dirname(__file__), "CHANGELOG.md")
    with open(changelog_path) as f:
        lines = f.readlines()
    log = lines[:lines.index("[//]: # (LINKS)\n") + 1]
    with open(changelog_path, "w") as f:
        f.writelines(log)
        f.writelines(get_changelog_links())


if __name__ == "__main__":
    build_api_table()
    update_changelog()
    sphinx_build()
