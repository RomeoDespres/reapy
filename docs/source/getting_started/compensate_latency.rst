Tuto: compensating audio device latency
=======================================


Introduction
------------

Now that you've learnt how to `create and run scripts in REAPER <hello_world.html>`_, let's try and make something useful.

The issue this tutorial solves is actually the one I wrote my very first REAPER script for. If you have a good quality audio interface, you may not have encountered that flaw most entry-level devices have: high latency. It was my case at the time, meaning every time I recorded something, it would end up off beat.

The thing is, it was off beat by a constant amount of time. So, after recording, I would always manually move the recorded item by this amount to the left, and everything would sound good. After doing this about a thousand times, I decided to write a script that would correct latency faster and more precisely than me, on a simple hit of the ``L`` key (for *latency*).

If you have latency problems, this may truly help you; if not, it will still be a good example of a simple script that does something better than shouting *Hello world*.


Building the script
-------------------

Create a new Python file ``compensate_latency.py``. We will only need four lines to perform our task, so let's throw them all at once before digging into details:

.. code:: py

    import reapy


    project = reapy.Project()

    for item in project.selected_items:
        item.position -= 0.16  # For a 160 ms latency

Don't know how you feel about it, but I tend to find it pretty straightforward: reading it is almost enough to understand what is going on.

1. ``import reapy``

We already know this first line. You will basically have it in all of your scripts.

2. ``project = reapy.Project()``

This line selects the currently active project and makes us able to control it later under the name ``project``. Note that if you pass an integer argument ``i`` to :class:`reapy.Project`, you'll be able to control the ``i``\ :sup:`th` project tab in REAPER (starting at 0) even though it is not the one that is currently active. For instance, ``project = reapy.Project(2)`` will allow to control the third project tab.

3. ``for item in project.selected_items:``

This line iterates though the list of all selected items in ``project``, that can be accessed with the ``project.selected_items`` property. Each selected item is read from this list and named ``item`` for the next indented block.

4. ``item.position -= 0.16``

The position of the item in seconds is available as ``item.position``. The ``-=`` operator decreases its left part (``item.position``) by its right part (``0.16``). My device latency was 160 ms, hence that value - replace it with your own. The whole line simply moves ``item`` 0.16 seconds to the left.

As this line is indented, it will be executed for each selected item. This allows you to correct several items at once if needed.

And that's all! Assign a keyboard shortcut or a toolbar button to this script as you've `previously learnt <hello_world.html>`_, and spend no more time compensating your audio device latency.
