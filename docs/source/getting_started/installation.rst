.. |pip| replace:: ``pip``
.. _pip: https://pip.pypa.io/en/stable/

Installation
============

.. note::

    Below are straightforward instructions for users that already have experience with using Python in a terminal. If you feel you need more explanation, head to `Detailed instructions`_.

reapy is available via ``pip``:

.. code-block:: bash

    $ pip install reapy

One additional step is required to let REAPER know reapy is available. Simply open REAPER, and run:

.. code-block:: bash

    $ python -c "import reapy; reapy.configure_reaper()"

Now restart REAPER, and you're all set!

Detailed instructions
---------------------

Not sure what the previous commands mean? The instructions below will guide you through all steps to get Python and reapy up and running.

Install Python
**************

You can check if you have Python installed by opening a terminal and running:

(Windows)

.. code-block:: bash

    py --version

(MacOS/Linux)

.. code-block:: bash

    python --version

If Python is installed, its version gets printed on the terminal. If you get an error or if your version of Python is 2.x.x, head to the `official Python download page <https://www.python.org/downloads>`_ and install Python 3.

.. note::

    Python 2 `officially died <https://www.python.org/dev/peps/pep-0373/#update-april-2014>`_ in January 2020, which is why reapy does not support it.

You may have read in `REAPER official documentation <https://www.reaper.fm/sdk/reascript/reascript.php#reascript_req_py>`_ that using Python for REAPER requires additional configuration steps. Don't spend time trying to reproduce them, reapy will do it for you.

Install reapy
*************

reapy can be installed with the standard Python package manager ``pip`` (documentation `here <https://pip.pypa.io/>`_). In the terminal, run:

.. code-block:: bash

    pip install reapy

.. note::

    Having both Python 2 and 3 installed may require to use ``pip3`` instead of ``pip`` . On Windows, if neither ``pip`` nor ``pip3`` works, ``py -m pip install reapy`` should do the trick.

Configure REAPER
****************

REAPER has to be configured to be able to use reapy. First, open REAPER, then run the following in a terminal:


(Windows)

.. code-block:: bash

    py -c "import reapy; reapy.configure_reaper()"

(MacOS/Linux)

.. code-block:: bash

    python -c "import reapy; reapy.configure_reaper()"

Finally, restart REAPER and you're good to go!
