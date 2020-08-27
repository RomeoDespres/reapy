"""Helper module to find python shared library.

This is a modified version of the script located at
https://gist.github.com/tkf/d980eee120611604c0b9b5fef5b8dae6.

Below are the original copyright and license:

    Copyright 2018, Takafumi Arakaki

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ctypes.util
import os
import sys
import sysconfig


__all__ = [
    "get_python_shared_library"
]


class _Dl_info(ctypes.Structure):

    _fields_ = [
        ("dli_fname", ctypes.c_char_p),
        ("dli_fbase", ctypes.c_void_p),
        ("dli_sname", ctypes.c_char_p),
        ("dli_saddr", ctypes.c_void_p),
    ]


def get_candidate_names():
    """Yield candidate file names for shared lib."""
    suffix = get_sharedlib_suffix()
    LDLIBRARY = sysconfig.get_config_var("LDLIBRARY")
    if LDLIBRARY:
        yield LDLIBRARY

    LIBRARY = sysconfig.get_config_var("LIBRARY")
    if LIBRARY:
        yield os.path.splitext(LIBRARY)[0] + suffix

    dlprefix = "" if is_windows() else "lib"
    sysdata = dict(
        v=sys.version_info,
        # VERSION is X.Y in Linux/macOS and XY in Windows:
        VERSION=(sysconfig.get_config_var("VERSION") or
                 "{v.major}.{v.minor}".format(v=sys.version_info)),
        ABIFLAGS=(sysconfig.get_config_var("ABIFLAGS") or
                  sysconfig.get_config_var("abiflags") or ""),
    )

    for stem in (
        "python{VERSION}{ABIFLAGS}".format(**sysdata),
        "python{VERSION}".format(**sysdata),
        "python{v.major}".format(**sysdata),
        "python"
    ):
        yield dlprefix + stem + suffix


def get_candidate_paths():
    """Yield candidate paths to shared lib."""
    yield get_linked_libpython()

    # List candidates for directories in which libpython may exist
    config_vars = "LIBPL", "srcdir", "LIBDIR"
    lib_dirs = list(map(sysconfig.get_config_var, config_vars))

    if is_windows():
        lib_dirs.append(os.path.join(os.path.dirname(sys.executable)))
    else:
        lib_dirs.append(os.path.join(
            os.path.dirname(os.path.dirname(sys.executable)),
            "lib"))

    # For macOS:
    lib_dirs.append(sysconfig.get_config_var("PYTHONFRAMEWORKPREFIX"))

    lib_dirs.append(sys.exec_prefix)
    lib_dirs.append(os.path.join(sys.exec_prefix, "lib"))

    lib_basenames = list(get_candidate_names())

    for directory in filter(bool, lib_dirs):
        for basename in lib_basenames:
            yield os.path.join(directory, basename)

    # In macOS and Windows, ctypes.util.find_library returns a full path:
    for basename in lib_basenames:
        yield ctypes.util.find_library(get_library_name(basename))


def get_library_name(name):
    """Convert file name to library name (no "lib" and ".so" etc.)."""
    suffix = get_sharedlib_suffix()
    if not is_windows() and name.startswith("lib"):
        name = name[len("lib"):]
    if suffix and name.endswith(suffix):
        name = name[:-len(suffix)]
    return name


def get_linked_libpython():
    """Return linked libpython using dladdr (in *nix).

    Return ``None`` if libpython is statically linked.
    """
    if is_windows():
        return
    libdl = ctypes.CDLL(ctypes.util.find_library("dl"))
    libdl.dladdr.argtypes = [ctypes.c_void_p, ctypes.POINTER(_Dl_info)]
    libdl.dladdr.restype = ctypes.c_int

    dlinfo = _Dl_info()
    retcode = libdl.dladdr(
        ctypes.cast(ctypes.pythonapi.Py_GetVersion, ctypes.c_void_p),
        ctypes.pointer(dlinfo))
    if retcode == 0:  # means error
        return
    path = os.path.realpath(dlinfo.dli_fname.decode())
    if path == os.path.realpath(sys.executable):
        return
    return path


def get_python_shared_library():
    """Return path to Python shared library (.dll, .dylib or .so).

    Returns
    -------
    path : str
        Path to the (hopefully) correct libpython.

    Raises
    ------
    FileNotFoundError
        When shared library could not be found.
    """
    for path in filter(is_valid, get_candidate_paths()):
        return path
    raise FileNotFoundError(
        "Could not find Python shared library. Please report this bug at "
        "https://github.com/RomeoDespres/reapy/issues/new so that we can "
        "support more cases."
    )


def get_sharedlib_suffix():
    """Return shared library suffix (.dll, .dylib or .so)."""
    suffix = sysconfig.get_config_var("SHLIB_SUFFIX")
    if suffix is None:
        if is_windows():
            suffix = ".dll"
        else:
            suffix = ".so"
    if is_apple():
        # sysconfig.get_config_var("SHLIB_SUFFIX") can be ".so" in macOS.
        # Let's not use the value from sysconfig.
        suffix = ".dylib"
    return suffix


def is_apple():
    """Return whether OS is MacOS or OSX."""
    return sys.platform == "darwin"


def is_valid(path):
    """Return whether path is a valid library path."""
    return (
        bool(path)
        and os.path.isabs(path)
        and os.path.exists(path)
        and (not is_apple() or path.endswith(".dylib"))
    )


def is_windows():
    """Return whether OS is Windows."""
    return os.name == "nt"
