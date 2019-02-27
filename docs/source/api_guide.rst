API guide
=========

This guide describes the main ``reapy`` functions and classes you will probably use in your ReaScripts. For more detailed documentation and access to the source code, check out the :ref:`modindex`.

.. contents:: Contents
    :local:
    :depth: 3
   

   
reapy
-----


The top-level package ``reapy`` includes general purpose functions that act at the level of REAPER itself, and not at the sub-level of a project, a track, etc.

All functions in `reapy.core.reaper.reaper <reapy.core.reaper.html#module-reapy.core.reaper.reaper>`_ are imported at the top-level, which means you can call ``reapy.function`` for any function ``function`` in this module.

    >>> import reapy
    >>> reapy.print("Hello world!")
    >>> reapy.clear_console()
    >>> reapy.get_reaper_version()
    '5.965/x64'
    >>> command_id = reapy.add_reascript(r"C:\path\to\my\reascript.py")
    >>> command_id
    53007
    >>> reapy.get_command_name(command_id)
    '_RSbcbf8f64cb92ff8062457098ee1194c7742e6431'

    
Improve performance with ``reapy.inside_reaper``
************************************************

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


Non-blocking loops inside REAPER with reapy.defer and reapy.at_exit
*******************************************************************

Inside REAPER, ReaScripts are run in the main thread. Thus, the REAPER interface is blocked until script execution is over. For that reason, you can't have infinite loops running in ReaScripts, which is why most GUI libraries that include a main loop detecting user actions can't be used in ReaScripts.

Of course, if you run reapy ReaScripts outside REAPER, there is no problem with infinite loops. Yet if you want to have loops running inside REAPER, you can make use of ``reapy.defer``.

Here is what ``reapy.defer`` does:

    **reapy**: hey REAPER I need you to call that function I wrote
    
    **REAPER**: man I can't spend my whole life running your scripts. I have stuff to do like... you know... making music
    
    **reapy**: all right well it's not that urgent. I only need you to call it soon, but not like just right now.
    
    **REAPER**: ok, well give it to me and I'll put it in my schedule. It should be done within the next 0.03 seconds.


REAPER typically executes around 30 deferred calls per second. The following example creates a loop that indefinitely prints integers to the REAPER console, without blocking REAPER::

    import reapy
        
    def stupid_loop(i):
        reapy.print(i)
        # hey REAPER could you do that again please?...
        reapy.defer(stupid_loop, i + 1)
    
    stupid_loop(0)  # Start the loop

When such a loop is running, the user might terminate it at some point, maybe by killing the ReaScript. If you need some clean-up code to be executed when it happens, you can make use of ``reapy.at_exit``. It tells REAPER to run the function whenever the script stops running (either because it reached its end, or because it has been manually terminated).

The following example opens a file and starts a loop that indefinitely writes integers to that file. Since we want the file to be closed when the user terminates script execution, call to its ``close`` method is deferred to ``reapy.at_exit``::

    import reapy
    
    file = open("somefile.txt", "w")
    
    def stupid_loop(i):
        file.write(i)
        reapy.defer(stupid_loop, i + 1)
    
    reapy.at_exit(file.close)  # Make sure REAPER cleans up after loop
    stupid_loop(0)  # Start the loop
    
    
reapy.Project
-------------

This is probably the class you will use the most. It represents a REAPER Project. To get the current project, just call ``reapy.Project()``. If you want to get a project that is not necessarily the current one, pass the ``index`` keyword argument to ``reapy.Project`` with the index of the corresponding tab in REAPER (starting at 0).

    >>> reapy.Project()  # Current project
    Project("(ReaProject*)0x0000000006D3AFF0")
    >>> reapy.Project(index=1)  # Project in REAPER's second tab
    Project("(ReaProject*)0x000000000440A2D0")
    >>> reapy.Project(index=-1)  # Current project
    Project("(ReaProject*)0x0000000006D3AFF0")

Projects have simple properties such as ``bpm``, ``is_current_project``, ``length``. You can manually set some of them, but not all.

    >>> project = reapy.Project()
    >>> project.bpm
    120.0
    >>> project.bpm = 100  # Set the tempo in REAPER to 100
    >>> project.length = 10  # Doesn't make sense to manually set length!
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute

They also have useful methods::

    >>> project.make_current_project()
    >>> track = project.add_track()
    >>> project.play()  # Hit the play button

The detailed class documentation is available `here <reapy.core.html#reapy.core.Project>`_.

reapy.Track
-----------

The easiest way to access Tracks is to get ``project.tracks``, which is the list of all tracks in the project. You can also get ``project.selected_tracks``.

Tracks have properties such as ``color``, ``n_items``, but also ``items`` or ``fxs`` which are the list of Items (or FXs) on the track.

    >>> project = reapy.Project()
    >>> track = project.tracks[2]  # Second track
    >>> track.name
    'KICK'
    
Detailed class documentation `here <reapy.core.html#reapy.core.Track>`_.

reapy.Send
**********

``Track.sends`` contains the list of Sends of a Track. You can also create new Sends with ``Track.add_send``. See `class documentation <reapy.core.html#reapy.core.Send>`_.

reapy.Envelope
**************

``Track.get_envelope`` allows you to get a Track's envelope by index, name or chunk name (i.e. special name for volume, pan, etc.)

    >>> envelope = track.get_envelope(index=0)
    >>> envelope.name
    'Volume'
    >>> track.get_envelope(name="Volume") == envelope
    True
    
See class documentation `here <reapy.core.html#reapy.core.Envelope>`_.

reapy.Item
----------

You can access Items via ``Project.selected_items`` or ``Track.items``. Detailed class documentation `here <reapy.core.html#reapy.core.Item>`_.

reapy.Take
**********

From Items, you can access takes via ``Item.takes`` or ``Item.active_take``. See the `class documentation <reapy.core.html#reapy.core.Take>`_.

reapy.Source
************

The property ``Take.source`` contains the Source of a Take. Sources have properties such as ``filename``, ``sample_rate``, or ``type`` (which can be ``"MIDI"``, ``"WAV"``, etc.). See the `class documentation <reapy.core.html#reapy.core.Source>`_.

reapy.FX
--------

You can get the list of FX on a track with ``Track.fxs``. You can also get the first virtual instrument on a Track with ``Track.instrument``.

Access and set the parameters of an FX as follows:

    >>> fx = track.fxs[0]
    >>> fx.n_params
    10
    >>> fx.params[0]
    0.5
    >>> fx.params[0] = 0.3  # Manually set the parameter
    >>> fx.params[0].name  # Params have names! (if the VST is nice)
    "Dry Gain"
    >>> fx.params["Dry Gain"]  # You can access them by name too
    0.3
    
See the full class documentation `here <reapy.core.html#reapy.core.FX>`_.