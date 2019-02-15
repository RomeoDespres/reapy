import reapy
from reapy import reascript_api as RPR
from reapy.tools import Program


class Track:

    def __init__(self, id, project=None):
        if isinstance(id, int):
            id = RPR.GetTrack(project.id, id)
        self.id = id
        
    def add_item(self):
        """
        Create new item on track and return it.
        
        Returns
        -------
        item : Item
            New item on track.
        """
        item_id = RPR.AddMediaItemToTrack(self.id)
        item = Item(item_id)
        return item
        
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
        if envelope.id == UNDEFINED_ENVELOPE_ID:
            raise UndefinedEnvelopeError(index, name, chunk_name)
        return envelope
        
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
        
    def unselect(self):
        """
        Unselect track.
        """
        RPR.SetTrackSelected(self.id, False)
  
  
from ..item.item import Item
from .envelope import Envelope, UndefinedEnvelopeError, UNDEFINED_ENVELOPE_ID
