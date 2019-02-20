.. reapy documentation master file, created by
   sphinx-quickstart on Fri Feb 15 11:18:25 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to reapy's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
``reapy`` is a nice pythonic wrapper around the quite unpythonic `ReaScript Python API <https://www.reaper.fm/sdk/reascript/reascripthelp.html#p>`_ for `REAPER <https://www.reaper.fm/>`_.

Getting Started
---------------

Installing
**********

1. First install from ``pip``::

    pip install python-reapy


2. Then in REAPER, execute a new ReaScript containing the following::

    import reapy
    reapy.config.enable_dist_api()

You can create new ReaScripts by going to *Actions > Show action list > Reascript : New...*.

3. You're all set! You can now import ``reapy`` from inside or outside REAPER as any standard Python module.

Instead of creating a new ReaScript containing::

    from reaper_python import *
    RPR_ShowConsoleMsg("Hello world!")

you can open your usual Python shell and type::

    >>> import reapy
    >>> reapy.print("Hello world!")

Usage
-----

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

When used from inside REAPER, ``reapy`` has almost identical performance than native ReaScript API. Yet when it is used from the outside, the performance is quite worse. More precisely, since external API calls are processed in a ``defer`` loop inside REAPER, there can only be around 30 to 60 of them per second.

In a time-critical context, you can make use of the ``reapy.tools.Program`` feature. It allows to execute arbitrary code inside REAPER, with input and output sent over the local network.

In the example below, one can see how to make use of ``Program`` to improve efficiency. Input parameters are passed to the program as ``Program.run`` keyword arguments. Required output values are specified as ``Program`` positional arguments after ``code`` (first positional argument).

Note that the modules ``reapy`` and ``reascript_api`` (as `RPR`) are always available in ``Program``. Any other needed module must be explicitly imported in the ``code``.

::
    >>> import reapy
    >>> project = reapy.Project() # Current project
    >>>
    >>> # Unefficient (and useless) call
    >>> start = time.time(); bpms = [project.bpm for _ in range(100)]
    >>> # Takes at least 3 seconds!
    >>>
    >>> # Efficient call
    >>> from reapy.tools import Program
    >>> code = """
    ... project = reapy.Project(project_id)
    ... bpms = [project.bpm for _ in range(100)]
    ... """
    >>> [bpms] = Program(code, "bpms").run(project_id = project.id)
    >>> # Takes 1/30 seconds (= one distant call)


Author
------

**Roméo Després** - `RomeoDespres <https://github.com/RomeoDespres>`_

License
-------

This project is licensed under the MIT License - see the `LICENSE.txt <https://github.com/RomeoDespres/reapy/blob/master/LICENSE.txt>`_ file for details.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
