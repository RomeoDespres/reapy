"""Defines class Project."""

import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.errors import RedoError, UndoError
import typing as ty
import typing_extensions as te


class Project(ReapyObject):
    """REAPER project."""
    id: str

    def __init__(self,
                 id: ty.Optional[ty.Union[int, str]] = None,
                 index: int = -1) -> None:
        """
        Build project either by ID or index.

        id : None, str or int, optional
            Project identifier.
            When None (default), `index is used instead.
            An integer is interpreted as the project index in GUI.
            A string starting with '(ReaProject*)0x' is interpreted
            as a ReaScript identifier.
            Otherwise, `id` is the project name. In that case, the .rpp
            extension is optional.
        index : int, optional
            Project index in GUI (default=-1, corresponds to current
            project).
        """
        ...

    def __eq__(self, other: object) -> bool:
        ...

    @property
    def _args(self) -> ty.Tuple[str]:
        ...

    @staticmethod
    def _from_name(name: str) -> 'Project':
        """Return project with corresponding name.

        Parameters
        ----------
        name : str
            Project file name. Including the extension ('.rpp')
            is optional.

        Returns
        -------
        Project

        Raises
        ------
        NameError
            If no project with the corresponding name is open.
        """
        ...

    def _get_track_by_name(self, name: str) -> ty.Optional[reapy.Track]:
        """Return first track with matching name."""
        ...

    def add_marker(self,
                   position: float,
                   name: str = "",
                   color: ty.Union[ty.Tuple[int], int] = 0) -> reapy.Marker:
        """
        Create new marker and return its index.

        Parameters
        ----------
        position : float
            Marker position in seconds.
        name : str, optional
            Marker name.
        color : int or tuple of int, optional
            Marker color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.

        Returns
        -------
        marker : reapy.Marker
            New marker.

        Notes
        -----
        If a marker with the same position and name already exists, no
        new marker will be created, and the existing marker index will
        be returned.
        """
        ...

    def add_region(self,
                   start: float,
                   end: float,
                   name: str = "",
                   color: ty.Union[ty.Tuple[int], int] = 0) -> reapy.Region:
        """
        Create new region and return its index.

        Parameters
        ----------
        start : float
            Region start in seconds.
        end : float
            Region end in seconds.
        name : str, optional
            Region name.
        color : int or tuple of int, optional
            Region color. Integers correspond to REAPER native colors.
            Tuple must be RGB triplets of integers between 0 and 255.

        Returns
        -------
        region : reapy.Region
            New region.
        """
        ...

    def add_track(self, index: int = 0, name: str = "") -> reapy.Track:
        """
        Add track at a specified index.

        Parameters
        ----------
        index : int
            Index at which to insert track.
        name : str, optional
            Name of created track.

        Returns
        -------
        track : Track
            New track.
        """
        ...

    @property
    def any_track_solo(self) -> bool:
        """
        Test whether any track is soloed in project.

        Returns
        -------
        any_track_solo : bool
            Whether any track is soloed in project.
        """
        ...

    def beats_to_time(self, beats: float) -> float:
        """
        Convert beats to time in seconds.

        Parameters
        ----------
        beats : float
            Time in beats

        Returns
        -------
        time : float
            Converted time in seconds.

        See also
        --------
        Project.time_to_beats
        """
        ...

    def begin_undo_block(self) -> None:
        """
        Start a new undo block.
        """
        ...

    @property
    def bpi(self) -> float:
        """
        Return project BPI (numerator of time signature).

        Returns
        -------
        bpi : float
            Numerator of time signature.
        """
        ...

    @property
    def bpm(self) -> float:
        """
        Project BPM (beats per minute).

        :type: float
        """
        ...

    @bpm.setter
    def bpm(self, bpm: float) -> None:
        """
        Set project BPM (beats per minute).

        Parameters
        ----------
        bpm : float
            Tempo in beats per minute.
        """
        ...

    @property
    def buffer_position(self) -> float:
        """
        Position of next audio block being processed in seconds.

        :type: float

        See also
        --------
        Project.play_position
            Latency-compensated actual-what-you-hear position.
        """
        ...

    def bypass_fx_on_all_tracks(self, bypass: bool = True) -> None:
        """
        Bypass or un-bypass FX on all tracks.

        Parameters
        ----------
        bypass : bool
            Whether to bypass or un-bypass FX.
        """
        ...

    @property
    def can_redo(self) -> bool:
        """
        Whether redo is possible.

        :type: bool
        """
        ...

    @property
    def can_undo(self) -> bool:
        """
        Whether undo is possible.

        :type: bool
        """
        ...

    @property
    def cursor_position(self) -> float:
        """
        Edit cursor position in seconds.

        :type: float
        """
        ...

    @cursor_position.setter
    def cursor_position(self, position: float) -> None:
        """
        Set edit cursor position.

        Parameters
        ----------
        position : float
            New edit cursor position in seconds.
        """
        ...

    def disarm_rec_on_all_tracks(self) -> None:
        """
        Disarm record on all tracks.
        """
        ...

    def end_undo_block(self, description: str = "") -> None:
        """
        End undo block.

        Parameters
        ----------
        description : str
            Undo block description.
        """
        ...

    @property
    def focused_fx(self) -> ty.Optional[reapy.FX]:
        """
        FX that has focus if any, else None.

        :type: FX or NoneType
        """
        ...

    def get_info_string(self, param_name: str) -> str:
        ...

    def get_info_value(self, param_name: str) -> float:
        ...

    @ty.overload
    def get_ext_state(self, section: str, key: str,
                      pickled: te.Literal[True]) -> object:
        """
        Return external state of project.

        Parameters
        ----------
        section : str
        key : str
        pickled: bool
            Whether data was pickled or not.

        Returns
        -------
        value : str
            If key or section does not exist an empty string is returned.
        """
        ...

    @ty.overload
    def get_ext_state(self, section: str, key: str,
                      pickled: te.Literal[False]) -> str:

        ...

    @ty.overload
    def get_ext_state(self, section: str, key: str,
                      pickled: bool = False) -> ty.Union[str, object]:

        ...

    def get_play_rate(self, position: float) -> float:
        """
        Return project play rate at a given position.

        Parameters
        ----------
        position : float
            Position in seconds.

        Returns
        -------
        play_rate : float
            Play rate at the given position.

        See also
        --------
        Project.play_rate
            Project play rate at the current position.
        """
        ...

    def get_selected_item(self, index: int) -> reapy.Item:
        """
        Return index-th selected item.

        Parameters
        ----------
        index : int
            Item index.

        Returns
        -------
        item : Item
            index-th selected item.
        """
        ...

    def get_selected_track(self, index: int) -> reapy.Track:
        """
        Return index-th selected track.

        Parameters
        ----------
        index : int
            Track index.

        Returns
        -------
        track : Track
            index-th selected track.
        """
        ...

    def glue_items(self, within_time_selection: bool = False) -> None:
        """
        Glue items (action shortcut).

        Parameters
        ----------
        within_time_selection : bool
            If True, glue items within time selection.
        """
        ...

    @property
    def is_dirty(self) -> bool:
        """
        Whether project is dirty (i.e. needing save).

        :type: bool
        """
        ...

    @property
    def is_current_project(self) -> bool:
        """
        Whether project is current project.

        :type: bool
        """
        ...

    @property
    def is_paused(self) -> bool:
        """
        Return whether project is paused.

        :type: bool
        """
        ...

    @property
    def is_playing(self) -> bool:
        """
        Return whether project is playing.

        :type: bool
        """
        ...

    @property
    def is_recording(self) -> bool:
        """
        Return whether project is recording.

        :type: bool
        """
        ...

    @property
    def is_stopped(self) -> bool:
        """
        Return whether project is stopped.

        :type: bool
        """
        ...

    @property
    def items(self) -> ty.List[reapy.Item]:
        """
        List of items in project.

        :type: list of Item
        """
        ...

    @property
    def length(self) -> float:
        """
        Project length in seconds.

        :type: float
        """
        ...

    @property
    def last_touched_fx(self
                        ) -> ty.Tuple[ty.Optional[reapy.FX], ty.Optional[int]]:
        """
        Last touched FX and corresponding parameter index.

        :type: FX, int or NoneType, NoneType

        Notes
        -----
        Only Track FX are detected by this property. If last touched
        FX is a Take FX, this property is ``(None, None)``.

        Examples
        --------
        >>> fx, index = project.last_touched_fx
        >>> fx.name
        'VSTi: ReaSamplOmatic5000 (Cockos)'
        >>> fx.params[index].name
        "Volume"
        """
        ...

    def make_current_project(self) -> ty.ContextManager[None]:
        """
        Set project as current project.

        Can also be used as a context manager to temporarily set
        the project as current project and then go back to the original
        situation.

        Examples
        --------
        >>> p1 = reapy.Project()  # current project
        >>> p2 = reapy.Project(1)  # other project
        >>> p2.make_current_project()  # now p2 is current project
        >>> with p1.make_current_project():
        ...     do_something()  # current project is temporarily p1
        >>> # and p2 is current project again
        """
        ...

    def mark_dirty(self) -> None:
        """
        Mark project as dirty (i.e. needing save).
        """
        ...

    @property
    def markers(self) -> ty.List[reapy.Marker]:
        """
        List of project markers.

        :type: list of reapy.Marker
        """
        ...

    @property
    def master_track(self) -> reapy.Track:
        """
        Project master track.

        :type: Track
        """
        ...

    def mute_all_tracks(self, mute: bool = True) -> None:
        """
        Mute or unmute all tracks.

        Parameters
        ----------
        mute : bool, optional
            Whether to mute or unmute all tracks (default=True).

        See also
        --------
        Project.unmute_all_tracks
        """
        ...

    @property
    def n_items(self) -> int:
        """
        Number of items in project.

        :type: int
        """
        ...

    @property
    def n_markers(self) -> int:
        """
        Number of markers in project.

        :type: int
        """
        ...

    @property
    def n_regions(self) -> int:
        """
        Number of regions in project.

        :type: int
        """
        ...

    @property
    def n_selected_items(self) -> int:
        """
        Number of selected media items.

        :type: int
        """
        ...

    @property
    def n_selected_tracks(self) -> int:
        """
        Number of selected tracks in project (excluding master).

        :type: int
        """
        ...

    @property
    def n_tempo_markers(self) -> int:
        """
        Number of tempo/time signature markers in project.

        :type: int
        """
        ...

    @property
    def n_tracks(self) -> int:
        """
        Number of tracks in project.

        :type: int
        """
        ...

    @property
    def name(self) -> str:
        """
        Project name.

        :type: str
        """
        ...

    def pause(self) -> None:
        """
        Hit pause button.
        """
        ...

    @property
    def path(self) -> str:
        """
        Project path.

        :type: str
        """
        ...

    def perform_action(self, action_id: int) -> None:
        """
        Perform action with ID `action_id` in the main Actions section.

        Parameters
        ----------
        action_id : int
            Action ID in the main Actions section.
        """
        ...

    def play(self) -> None:
        """
        Hit play button.
        """
        ...

    @property
    def play_position(self) -> float:
        """
        Latency-compensated actual-what-you-hear position in seconds.

        :type: float

        See also
        --------
        Project.buffer_position
            Position of next audio block being processed.
        """
        ...

    @property
    def play_rate(self) -> float:
        """
        Project play rate at the cursor position.

        :type: float

        See also
        --------
        Project.get_play_rate
            Return project play rate at a specified time.
        """
        ...

    def redo(self) -> None:
        """
        Redo last action.

        Raises
        ------
        RedoError
            If impossible to redo.
        """
        ...

    @property
    def regions(self) -> ty.List[reapy.Region]:
        """
        List of project regions.

        :type: list of reapy.Region
        """
        ...

    def save(self, force_save_as: bool = False) -> None:
        """
        Save project.

        Parameters
        ----------
        force_save_as : bool
            Force using "Save as" instead of "Save".
        """
        ...

    def select(self,
               start: float,
               end: ty.Optional[float] = None,
               length: ty.Optional[float] = None) -> None:
        ...

    def select_all_items(self, selected: bool = True) -> None:
        """
        Select or unselect all items, depending on `selected`.

        Parameters
        ----------
        selected : bool
            Whether to select or unselect items.
        """
        ...

    def select_all_tracks(self) -> None:
        """Select all tracks."""
        ...

    @property
    def selected_envelope(self) -> ty.Optional[reapy.Envelope]:
        """
        Project selected envelope.

        :type: reapy.Envelope or None
        """
        ...

    @property
    def selected_items(self) -> ty.List[reapy.Item]:
        """
        List of all selected items.

        :type: list of Item

        See also
        --------
        Project.get_selected_item
            Return a specific selected item.
        """
        ...

    @property
    def selected_tracks(self) -> ty.List[reapy.Track]:
        """
        List of selected tracks (excluding master).

        :type: list of Track
        """
        ...

    @selected_tracks.setter
    def selected_tracks(self, tracks: ty.List[reapy.Track]) -> None:
        ...

    def set_info_string(self, param_name: str, param_string: str) -> None:
        """
        Parameters
        ----------
        param_name : str
            MARKER_GUID:X : get the GUID (unique ID) of the marker or region
                with index X, where X is the index passed to
                EnumProjectMarkers, not necessarily the displayed number
            RECORD_PATH :
                recording directory -- may be blank or a relative path,
                to get the effective path see GetProjectPathEx()
            RENDER_FILE : render directory
            RENDER_PATTERN : render file name (may contain wildcards)
            RENDER_FORMAT : base64-encoded sink configuration
                (see project files, etc). Callers can also pass a simple
                4-byte string (non-base64-encoded), e.g. "evaw" or "l3pm",
                to use default settings for that sink type.
            RENDER_FORMAT2 : base64-encoded secondary sink configuration.
                Callers can also pass a simple 4-byte string (non-base64-encoded),
                e.g. "evaw" or "l3pm", to use default settings for
                that sink type, or "" to disable secondary render.
                Formats available on this machine:
                "wave" "aiff" "iso " "ddp " "flac" "mp3l" "oggv" "OggS"
                "FFMP" "GIF " "LCF " "wvpk"
        param_string : str
        """
        ...

    def set_info_value(self, param_name: str, param_value: float) -> None:
        """
        Parameters
        ----------
        param_name : str
            RENDER_SETTINGS : &(1|2)=0:master mix, &1=stems+master mix,
                &2=stems only, &4=multichannel tracks to multichannel files,
                &8=use render matrix, &16=tracks with only mono media
                to mono files, &32=selected media items,
                &64=selected media items via master
            RENDER_BOUNDSFLAG : 0=custom time bounds, 1=entire project,
                2=time selection, 3=all project regions,
                4=selected media items, 5=selected project regions
            RENDER_CHANNELS : number of channels in rendered file
            RENDER_SRATE : sample rate of rendered file
                (or 0 for project sample rate)
            RENDER_STARTPOS : render start time when RENDER_BOUNDSFLAG=0
            RENDER_ENDPOS : render end time when RENDER_BOUNDSFLAG=0
            RENDER_TAILFLAG : apply render tail setting when rendering:
                &1=custom time bounds, &2=entire project, &4=time selection,
                &8=all project regions, &16=selected media items,
                &32=selected project regions
            RENDER_TAILMS : tail length in ms to render
                (only used if RENDER_BOUNDSFLAG and RENDER_TAILFLAG are set)
            RENDER_ADDTOPROJ : 1=add rendered files to project
            RENDER_DITHER : &1=dither, &2=noise shaping, &4=dither stems,
                &8=noise shaping on stems
            PROJECT_SRATE : samplerate (ignored unless PROJECT_SRATE_USE set)
            PROJECT_SRATE_USE : set to 1 if project samplerate is used
        param_value : float
        """
        ...

    @ty.overload
    def set_ext_state(self, section: str, key: str, value: str,
                      pickled: te.Literal[False]) -> int:
        """
        Set external state of project.

        Parameters
        ----------
        section : str
        key : str
        value : Union[Any, str]
            State value. Will be dumped to str using either `pickle` if
            `pickled` is `True` or `json`. Length of the dumped value
            must not be over 2**31 - 2.
        pickled : bool, optional
            Data will be pickled with the last version if True.
            If you using mypy as type checker, typing_extensions.Literal[True]
            has to be used for `pickled`.

        Raises
        ------
        ValueError
            If dumped `value` has length over 2**31 - 2.
        """
        ...

    @ty.overload
    def set_ext_state(self, section: str, key: str, value: ty.Any,
                      pickled: te.Literal[True]) -> int: ...

    @ty.overload
    def set_ext_state(self, section: str, key: str, value: str,
                      pickled: bool = False) -> int: ...

    def solo_all_tracks(self) -> None:
        """
        Solo all tracks in project.

        See also
        --------
        Project.unsolo_all_tracks
        """
        ...

    def stop(self) -> None:
        """
        Hit stop button.
        """
        ...

    @property
    def time_selection(self) -> reapy.TimeSelection:
        """
        Project time selection.

        time_selection : reapy.TimeSelection

        Can be set and deleted as follows:

        >>> project = reapy.Project()
        >>> project.time_selection = 3, 8  # seconds
        >>> del project.time_selection
        """
        ...

    @time_selection.setter
    def time_selection(self, selection: ty.Tuple[float, float]) -> None:
        """
        Set time selection bounds.

        Parameters
        ----------
        selection : (float, float)
            Start and end of new time selection in seconds.
        """
        ...

    @time_selection.deleter
    def time_selection(self) -> None:
        """
        Delete current time selection.
        """
        ...

    @property
    def time_signature(self) -> ty.Tuple[float, float]:
        """
        Project time signature.

        This does not reflect tempo envelopes but is purely what is set in the
        project settings.

        bpm : float
            Project BPM (beats per minute)
        bpi : float
            Project BPI (numerator of time signature)
        """
        ...

    def time_to_beats(self, time: float) -> float:
        """
        Convert time in seconds to beats.

        Parameters
        ----------
        time : float
            Time in seconds.

        Returns
        -------
        beats : float
            Time in beats.

        See also
        --------
        Projecr.beats_to_time
        """
        ...

    @property
    def tracks(self) -> reapy.TrackList:
        """
        List of project tracks.

        :type: TrackList
        """
        ...

    def undo(self) -> None:
        """
        Undo last action.

        Raises
        ------
        UndoError
            If impossible to undo.
        """
        ...

    def unmute_all_tracks(self) -> None:
        """
        Unmute all tracks.
        """
        ...

    def unselect_all_tracks(self) -> None:
        """Unselect all tracks."""
        ...

    def unsolo_all_tracks(self) -> None:
        """
        Unsolo all tracks in project.

        See also
        --------
        Project.solo_all_tracks
        """
        ...


class _MakeCurrentProject:
    """Context manager used by Project.make_current_project."""
    current_project: Project

    def __init__(self, project: Project) -> None:
        ...

    def __enter__(self) -> None:
        ...

    def __exit__(self, exc_type: ty.Any, exc_val: ty.Any,
                 exc_tb: ty.Any) -> None:
        ...
