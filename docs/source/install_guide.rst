Installation and uninstallation guide
=====================================

.. contents:: Contents
    :local:
    :depth: 2


Installation
------------

pip
***

``reapy`` can be installed *via* ``pip`` by running::

    pip install python-reapy

If Python is already enabled in REAPER, and if you only wish to use ``reapy`` from inside REAPER, you're done! Otherwise, keep reading.

Get configuration infos
***********************

In a terminal, run::

    py -m reapy

You should get something like::

    C:\Users\username\AppData\Local\Programs\Python\Python37\Lib\site-packages\reapy\tools\dist_program.py:14: DisabledDistAPIWarning: Can't reach distant API. Please start REAPER, or call reapy.config.enable_dist_api() from inside REAPER to enable distant API.
      warnings.warn(DisabledDistAPIWarning())

    ======================
      reapy config infos
    ======================

    Python DLL
    ----------
        C:\Users\username\AppData\Local\Programs\Python\Python37\python37.dll

    Enable or disable reapy dist API
    --------------------------------
    Enable dist API
         C:\Users\username\AppData\Local\Programs\Python\Python37\Lib\site-packages\reapy\reascripts\enable_dist_api.py

    Disable dist API
         C:\Users\username\AppData\Local\Programs\Python\Python37\Lib\site-packages\reapy\reascripts\disable_dist_api.py

Enable Python in REAPER
***********************

If Python is already enabled in REAPER, please skip this step. Otherwise, since Python is not natively enabled in REAPER, you have to configure it.

In REAPER, go to *Options > Preferences... > Plug-ins > ReaScript*. Check *Enable Python for use with ReaScript*, and fill *Custom path to Python dll directory* and *Force ReaScript to use specific Python .dll* with the directory path and the file name of the Python DLL as provided by the previous section.

Restart REAPER.

Enable ``reapy`` distant API
****************************

If you want to be able to use ``reapy`` outside REAPER, you need to enable its distant API.

Go to *Actions > Show action list > Reascript : Load...* and browse for the script path previously displayed in the config infos. A new Action appears called "Script: enable_dist_api.py". Double-click on it and restart REAPER.

You're all set! Check out the `API guide <api_guide.html>`_ and the `Translation table <api_table.html>`_ for more information about how to use ``reapy``.


Uninstallation
--------------

To uninstall ``reapy``, first get the path to ``disable_dist_api.py`` by displaying ``reapy`` config infos (see `above <#get-configuration-infos>`_ ).

In REAPER, go to *Actions > Show action list > Reascript : Load...* and browse for the path. A new Action appears called "Script: disable_dist_api.py". Double-click on it.

Finally, run::

    pip uninstall python-reapy

``reapy`` is now uninstalled from your machine.
