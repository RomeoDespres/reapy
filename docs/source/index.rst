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
   Module Index <py-modindex.html#://>
   Index <genindex.html#://>
   
``reapy`` is a nice pythonic wrapper around the quite unpythonic `ReaScript Python API <https://www.reaper.fm/sdk/reascript/reascripthelp.html#p>`_ for `REAPER <https://www.reaper.fm/>`_.

Installation
------------

1. First install from ``pip``::

    pip install python-reapy

2. Run::

    python -m reapy

Paths to your Python DLL and to ``reapy`` configuration scripts get printed.

3. If you haven't enabled Python in REAPER yet, go to *Options > Preferences... > Plug-ins > ReaScript*. Check *Enable Python for use with ReaScript*, and fill *Custom path to Python dll directory* and *Force ReaScript to use specific Python .dll* with the directory path and the file name of the Python DLL.

4. Enable ``reapy`` dist API by running the corresponding ReaScript (*Actions > Show action list > Reascript : Load...* and browse for the script path).

You're all set! You can now import ``reapy`` from inside or outside REAPER as any standard Python module.

Instead of creating a new ReaScript containing::

    >>> from reaper_python import *
    >>> RPR_ShowConsoleMsg("Hello world!")

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

Although this method should be sufficient in most cases, note that optimality is only reached by making use of ``reapy.tools.Program`` (see documentation `here <reapy.tools.html#reapy.tools.program.Program>`_).
    
More
****
Check out the `API guide <api_guide.html>`_ to discover ``reapy`` classes.

Contributing
------------

For now, about a third of ReaScript API has a ``reapy`` counterpart, the docs are far from great, and many bugs are waiting to be found. Feel free to improve the project by checking the `contribution guide <https://github.com/RomeoDespres/reapy/blob/master/CONTRIBUTING.md>`_ !

Author
------

**Roméo Després** - `RomeoDespres <https://github.com/RomeoDespres>`_

License
-------

This project is licensed under the MIT License - see the `LICENSE.txt <https://github.com/RomeoDespres/reapy/blob/master/LICENSE.txt>`_ file for details.
