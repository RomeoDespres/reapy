import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program
from reapy.errors import UndefinedEnvelopeError


class Track(ReapyObject):

    _class_name = "Track"

    def __init__(self, id, project=None):
        if isinstance(id, int):
            id = RPR.GetTrack(project.id, id)
        self.id = id
    
    @property
    def _args(self):
        return (self.id,)
        
    def add_item(self, start=0, end=None, length=0):
        """
        Create new item on track and return it.
        
        Parameters
        ----------
        start : float, optional
            New item start in seconds (default=0).
        end : float, optional
            New item end in seconds (default None). If None, `length`
            is used instead.
        length : float, optional
            New item length in seconds (default 0).
        
        Returns
        -------
        item : Item
            New item on track.
        """
        if end is None:
            end = start + length
        code = """
        item_id = RPR.AddMediaItemToTrack(track_id)
        item = reapy.Item(item_id)
        item.position = start
        item.length = end - start
        """
        item = Program(code, "item").run(
            track_id=self.id, start=start, end=end
        )[0]
        return item
        
    def add_midi_item(self, start=0, end=1, quantize=False):
        """
        Add empty MIDI item to track and return it.
        
        Parameters
        ----------
        start : float, optional
            New item start in seconds (or beats if `quantize`=True).
        end : float, optional
            New item end in seconds (or beats if `quantize`=True).
        quantize : boo, optional
            Whether to count time in beats (True) or seconds (False,
            default).
        """
        item_id = RPR.CreateNewMIDIItemInProj(self.id, start, end, quantize)
        item = MIDIItem(item_id)
        return item
        
    def add_send(self, destination=None):
        """
        Add send to track and return it.
        
        Parameters
        ----------
        destination : Track or None
            Send destination (default=None). If None, destination is
            set to hardware output.
            
        Returns
        -------
        send : Send
            New send on track.
        """
        if isinstance(destination, Track):
            destination = destination.id
        send_id = RPR.CreateTrackSend(self.id, destination)
        type = "hardware" if destination is None else "send"
        send = Send(self, send_id, type=type)
        return send
        
    @property
    def automation_mode(self):
        """
        Return track automation mode.
        
        Returns
        -------
        automation_mode : str
            One of the following values:
                "latch"
                "latch preview"
                "read"
                "touch"
                "trim/read"
                "write"
        """
        modes = "trim/read", "read", "touch", "write", "latch", "latch preview"
        automation_mode = modes[RPR.GetTrackAutomationMode(self.id)]
        return automation_mode
        
    @automation_mode.setter
    def automation_mode(self, mode):
        """
        Set track automation mode.
        
        Parameters
        -------
        mode : str
            One of the following values:
                "latch"
                "latch preview"
                "read"
                "touch"
                "trim/read"
                "write"
        """
        modes = "trim/read", "read", "touch", "write", "latch", "latch preview"
        RPR.SetTrackAutomationMode(self.id, modes.index(mode))
        
    @property
    def color(self):
        """
        Return track color in RGB format.
        
        Returns
        -------
        r : int
            Red value of track color.
        g : int
            Green value of track color.
        b : int
            Blue value of track color.
        """
        native_color = RPR.GetTrackColor(self.id)
        r, g, b = reapy.rgb_from_native(native_color)
        return r, g, b
        
    @color.setter
    def color(self, color):
        """
        Set track color to `color`
        
        Parameters
        ----------
        color : tuple
            Triplet of integers between 0 and 255 corresponding to RGB
            values.
        """
        native_color = reapy.rgb_to_native(color)
        RPR.SetTrackColor(self.id, native_color)
        
    def delete(self):
        """
        Delete track.
        """
        RPR.DeleteTrack(self.id)
        
    @property
    def depth(self):
        """
        Return track depth.
        
        Returns
        -------
        depth : int
            Track depth.
        """
        depth = RPR.GetTrackDepth(self.id)
        return depth
        
    @property
    def fxs(self):
        """
        Return list of FXs on track.
        
        Returns
        -------
        fxs : list of TrackFX
            List of FXs on track.
        """
        fxs = [TrackFX(self, i) for i in range(self.n_fxs)]
        return fxs
        
    def get_envelope(self, index=None, name=None, chunk_name=None):
        """
        Return track envelope for a given index, name or chunk name.
        
        Parameters
        ----------
        index : int, optional
            Envelope index.
        name : str, optional
            Envelope name.
        chunk_name : str, optional
            Built-in envelope configuration chunk name, e.g. "<VOLENV".
            
        Returns
        -------
        envelope : Envelope
            Track envelope.
        """
        if index is not None:
            function, arg = RPR.GetTrackEnvelope, index
        elif name is not None:
            function, arg = RPR.GetTrackEnvelopeByName, name
        else:
            message = (
                "One of `index`, `name` or `chunk_name` must be specified"
            )
            assert chunk_name is not None, message
            function, arg = RPR.GetTrackEnvelopeByChunkName, chunk_name
        envelope = Envelope(function(self.id, arg))
        if not envelope._is_defined:
            raise UndefinedEnvelopeError(index, name, chunk_name)
        return envelope
    
    @property
    def instrument(self):
        """
        Return first instrument FX on track if it exists.
        
        Returns
        -------
        instrument : TrackFX or None
            First instrument FX on track if it exists, else None.
        """
        fx_index = RPR.TrackFX_GetInstrument(self.id)
        instrument = None if fx_index == -1 else TrackFX(self, fx_index)
        return instrument
        
    @property
    def items(self):
        """
        Return list of items on track.

        Returns
        -------
        items : list of Item
            List of items on track.
        """
        code = """
        n_items = RPR.CountTrackMediaItems(track_id)
        item_ids = [
            RPR.GetTrackMediaItem(track_id, i) for i in range(n_items)
        ]
        """
        item_ids = Program(code, "item_ids").run(track_id=self.id)[0]
        items = [Item(item_id) for item_id in item_ids]
        return items
        
    @property
    def is_selected(self):
        """
        Return whether track is selected.
        
        Returns
        -------
        is_selected : bool
            Whether track is selected.
        """
        is_selected = bool(RPR.IsTrackSelected(self.id))
        return is_selected
        
    @is_selected.setter
    def is_selected(self, selected):
        """
        Select or unselect track.
        
        Parameters
        ----------
        selected : bool
            Whether to select or unselect track.
        """
        if selected:
            self.select()
        else:
            self.unselect()
            
    def make_only_selected_track(self):
        """
        Make track the only selected track in parent project.
        """
        RPR.SetOnlyTrackSelected(self.id)
            
    @property
    def n_envelopes(self):
        """
        Return number of envelopes on track.
        
        Returns
        -------
        n_envelopes : int
            Number of envelopes on track.
        """
        n_envelopes = RPR.CountTrackEnvelopes(self.id)
        return n_envelopes
        
    @property
    def n_fxs(self):
        """
        Return number of FXs on track.
        
        Returns
        -------
        n_fxs : int
            Number of FXs on track.
        """
        n_fxs = RPR.TrackFX_GetCount(self.id)
        return n_fxs
        
    @property
    def n_hardware_sends(self):
        n_hardware_sends = RPR.GetTrackNumSends(self.id, 1)
        return n_hardware_sends
            
    @property
    def n_items(self):
        """
        Return number of items on track.
        
        Returns
        -------
        n_items : int
            Number of items on track.
        """
        n_items = RPR.CountTrackMediaItems(self.id)
        return n_items
        
    @property
    def n_receives(self):
        n_receives = RPR.GetTrackNumSends(self.id, -1)
        return n_receives
        
    @property
    def n_sends(self):
        n_sends = RPR.GetTrackNumSends(self.id, 0)
        return n_sends
        
    @property
    def name(self):
        """
        Return track name.
        
        Returns
        -------
        name : str
            Track name ("MASTER" for master track, "Track N" if track
            has no name).
        """
        _, _, name, _ = RPR.GetTrackName(self.id, "", 2048)
        return name
        
    def select(self):
        """
        Select track.
        """
        RPR.SetTrackSelected(self.id, True)
        
    @property
    def sends(self):
        code = """
        sends = [Send(track, i, type="send") for i in range(track.n_sends)]
        """
        sends = Program(code, "sends").run(track=self)[0]
        return sends
        
    def unselect(self):
        """
        Unselect track.
        """
        RPR.SetTrackSelected(self.id, False)
  
  
from ..item.item import Item, MIDIItem
from .envelope import Envelope
from .send import Send
from .track_fx import TrackFX
