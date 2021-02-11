.. reapy documentation master file, created by
   sphinx-quickstart on Fri Feb 15 11:18:25 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to reapy's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :hidden:

   Api guide <api_guide.html#://>
   Translation Table <api_table.html#://>
   Install or uninstall reapy <install_guide.html#://>
   Module Index <py-modindex.html#://>
   Index <genindex.html#://>

.. contents:: Contents
    :local:
    :depth: 3

``reapy`` is a nice pythonic wrapper around the quite unpythonic `ReaScript Python API <https://www.reaper.fm/sdk/reascript/reascripthelp.html#p>`_ for `REAPER <https://www.reaper.fm/>`_.

Installation
------------

See the `Installation guide <install_guide.html>`_ for installation instructions.

Usage
-----

``reapy`` has two main features: it allows nice pythonic code, and interactions with REAPER from the outside. Instead of creating a new ReaScript containing::

    >>> from reaper_python import *
    >>> RPR_ShowConsoleMsg("Hello world!")

you can open your usual Python shell and type::

    >>> import reapy
    >>> reapy.print("Hello world!")

ReaScript API
*************

All ReaScript API functions are available in ``reapy`` in the sub-module ``reapy.reascript_api``. Note that in ReaScript Python API, all function names start with ``"RPR_"``. That unnecessary pseudo-namespace has been removed in ``reapy``. Thus, you shall call ``reapy.reascript_api.GetCursorPosition`` in order to trigger ``reaper_python.RPR_GetCursorPosition``. See example below::

    >>> from reapy import reascript_api as RPR
    >>> RPR.GetCursorPosition()
    0.0
    >>> RPR.SetEditCurPos(1, True, True)
    >>> RPR.GetCursorPosition()
    1.0


``reapy`` API
*************

The purpose of ``reapy`` is to provide a more pythonic API as a substitute for ReaScript API. Below is the ``reapy`` way of executing the example above::

    >>> import reapy
    >>> project = reapy.Project() # current project
    >>> project.cursor_position
    0.0
    >>> project.cursor_position = 1
    >>> project.cursor_position
    1.0

The `Translation table <api_table.html>`_ matches ReaScript functions with their ``reapy`` counterparts.

Performance
***********

When used from inside REAPER, ``reapy`` has almost identical performance than native ReaScript API. Yet when it is used from the outside, the performance is quite worse. More precisely, since external API calls are processed in a ``defer`` loop inside REAPER, there can only be around 30 to 60 of them per second. In a time-critical context, you should make use of the ``reapy.inside_reaper`` context manager.


    >>> import reapy
    >>> project = reapy.Project() # Current project
    >>>
    >>> # Unefficient (and useless) call
    >>> bpms = [project.bpm for _ in range(1000)] # Takes at least 30 seconds...
    >>>
    >>> # Efficient call
    >>> with reapy.inside_reaper():
    ...     bpms = [project.bpm for _ in range(1000)]
    ...
    >>> # Takes only 0.1 second!

A small overhead due to sending function and arguments over the network will
still occur each time a ``reapy`` function is called from outside REAPER. When
running the same function many times in a row (e.g. over a thousand times), using
:py:func:`reapy.map <reapy.core.map>` may significantly increase performance.
See its documentation for more details.

API documentation
-----------------

Check out the `API guide <api_guide.html>`_ and the `Translation table <api_table.html>`_ for more information about how to use ``reapy``.

Contributing
------------

For now, about a third of ReaScript API has a ``reapy`` counterpart, the docs are far from great, and many bugs are waiting to be found. Feel free to improve the project by checking the `contribution guide <https://github.com/RomeoDespres/reapy/blob/master/CONTRIBUTING.md>`_ !

Author
------

**Roméo Després** - `RomeoDespres <https://github.com/RomeoDespres>`_

License
-------

This project is licensed under the MIT License - see the `LICENSE.txt <https://github.com/RomeoDespres/reapy/blob/master/LICENSE.txt>`_ file for details.
