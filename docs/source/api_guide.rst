API guide
=========

This guide describes the main ``reapy`` classes you will probably use in your ReaScripts, and the way to build them. For more detailed documentation and access to the source code, check out the :ref:`modindex`.

.. contents:: Contents
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