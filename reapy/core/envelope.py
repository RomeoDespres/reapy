import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Envelope(ReapyObject):

    def __init__(self, parent, id):
        self.id = id
        self._parent = parent

    @property
    def _args(self):
        return (self.parent, self.id)

    def add_item(self, position=0., length=1., pool=0):
        """
        Add automation item to envelope.

        Parameters
        ----------
        position : float, optional
            New item position in seconds (default=0).
        length : float
            New item length in seconds (default=0).
        pool : int
            New item pool index. If >= 0 the automation item will be a
            new instance of that pool (which will be created as an
            empty instance if it does not exist).

        Returns
        -------
        item : reapy.AutomationItem
            New automation item.
        """
        item_index = RPR.InsertAutomationItem(self.id, pool, position, length)
        item = reapy.AutomationItem(envelope=self, index=item_index)
        return item

    def delete_points_in_range(self, start, end):
        """
        Delete envelope points between `start` and `end`.

        Parameters
        ----------
        start : float
            Range start in seconds.
        end : float
            Range end in seconds.
        """
        RPR.DeleteEnvelopePointRange(self.id, start, end)

    @reapy.inside_reaper()
    def get_derivatives(self, time, raw=False):
        """
        Return envelope derivatives of order 1, 2, 3 at a given time.

        Parameters
        ----------
        time : float
            Time in seconds.
        raw : bool, optional
            Whether to return raw values or the human-readable version
            which is printed in REAPER GUI (default=False).

        Returns
        -------
        d, d2, d3 : float
            First, second and third order derivatives.

        Examples
        --------
        >>> envelope = track.envelopes["Pan"]
        >>> envelope.get_derivatives(10, raw=True)
        (0.10635556358181712, 0.2127113398749741, 0.21271155258652666)
        >>> envelope.get_value(10)  # human-readable
        ('10%L', '21%L', '21%L')
        """
        d, d2, d3 = RPR.Envelope_Evaluate(self.id, time, 1, 1, 0, 0, 0, 0)[6:]
        if not raw:
            d = RPR.Envelope_FormatValue(self.id, d, "", 2048)[2]
            d2 = RPR.Envelope_FormatValue(self.id, d2, "", 2048)[2]
            d3 = RPR.Envelope_FormatValue(self.id, d3, "", 2048)[2]
        return d, d2, d3

    @reapy.inside_reaper()
    def get_value(self, time, raw=False):
        """
        Return envelope value at a given time.

        Parameters
        ----------
        time : float
            Time in seconds.
        raw : bool, optional
            Whether to return raw value or its human-readable version,
            which is the one that is printed in REAPER GUI
            (default=False).

        Returns
        -------
        value : float or str
            Envelope value.

        Examples
        --------
        >>> envelope = track.envelopes["Pan"]
        >>> envelope.get_value(10, raw=True)
        -0.5145481809245827
        >>> envelope.get_value(10)  # human-readable
        '51%R'
        """
        value = RPR.Envelope_Evaluate(self.id, time, 0, 0, 0, 0, 0, 0)[5]
        if not raw:
            value = RPR.Envelope_FormatValue(self.id, value, "", 2048)[2]
        return value

    @property
    def items(self):
        """
        List of automation items in envelope.

        :type: list of reapy.AutomationItem
        """
        items = [reapy.AutomationItem(self, i) for i in range(self.n_items)]
        return items

    @property
    def n_items(self):
        """
        Number of automation items in envelope.

        :type: int
        """
        n_items = RPR.CountAutomationItems(self.id)
        return n_items

    @property
    def n_points(self):
        """
        Number of points in envelope.

        :type: int
        """
        n_points = RPR.CountEnvelopePoints(self.id)
        return n_points

    @property
    def name(self):
        """
        Envelope name.

        :type: str
        """
        name = RPR.GetEnvelopeName(self.id, "", 2048)[2]
        return name

    @property
    def parent(self):
        """
        Envelope parent.

        :type: Take or Track
        """
        return self._parent


class EnvelopeList(ReapyObject):

    """
    Container class for the list of envelopes on a Take or Track.

    Envelopes can be accessed from the EnvelopeList either by index,
    name or chunk_name (e.g. "<VOLENV").

    Examples
    --------
    >>> len(track.envelopes)
    2
    >>> envelope = track.envelopes[0]
    >>> envelope.name
    'Volume'
    >>> envelope == track.envelopes["Volume"]
    True
    >>> envelope == track.envelopes["<VOLENV"]
    True
    >>> [e.name for e in track.envelopes]
    ['Volume', 'Pan']
    """

    def __init__(self, parent):
        self.parent = parent

    @property
    def _args(self):
        return (self.parent,)

    def __getitem__(self, key):
        if isinstance(key, int):
            callback = RPR.GetTrackEnvelope
        elif isinstance(key, str) and not key.startswith("<"):
            callback = RPR.GetTrackEnvelopeByName
        else:
            callback = RPR.GetTrackEnvelopeByChunkName
        envelope = Envelope(self, callback(self.parent.id, key))
        if not envelope._is_defined:
            raise KeyError("No envelope for key {}".format(repr(key)))
        return envelope

    def __len__(self):
        return self.parent.n_envelopes
