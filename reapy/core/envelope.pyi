import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class Envelope(ReapyObject):
    id: int
    _parent: ty.Union[ty.Type[reapy.Take], ty.Type[reapy.Track]]

    def __init__(self, parent: ReapyObject, id: int) -> None:
        ...

    @property
    def _args(self) -> ty.Tuple[ReapyObject, int]:
        ...

    def add_item(self, position: float = 0., length: float = 1.,
                 pool: int = 0) -> reapy.AutomationItem:
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
        ...

    def delete_points_in_range(self, start: float, end: float) -> None:
        """
        Delete envelope points between `start` and `end`.

        Parameters
        ----------
        start : float
            Range start in seconds.
        end : float
            Range end in seconds.
        """
        ...

    @reapy.inside_reaper()
    def get_derivatives(self, time: float,
                        raw: bool = False) -> ty.Tuple[float, float, float]:
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
        ...

    @reapy.inside_reaper()
    def get_value(self, time: float,
                  raw: bool = False) -> ty.Union[float, str]:
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
        ...

    @property
    def items(self) -> ty.List[reapy.AutomationItem]:
        """
        List of automation items in envelope.

        :type: list of reapy.AutomationItem
        """
        ...

    @property
    def n_items(self) -> int:
        """
        Number of automation items in envelope.

        :type: int
        """
        ...

    @property
    def n_points(self) -> int:
        """
        Number of points in envelope.

        :type: int
        """
        ...

    @property
    def name(self) -> str:
        """
        Envelope name.

        :type: str
        """
        ...

    @property
    def parent(self) -> ty.Union[ty.Type[reapy.Take], ty.Type[reapy.Track]]:
        """
        Envelope parent.

        :type: Take or Track
        """
        ...


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
    parent: ty.Union[ty.Type[reapy.Take], ty.Type[reapy.Track]]

    def __init__(self,
                 parent: ty.Union[ty.Type[reapy.Take], ty.Type[reapy.Track]]
                 ) -> None:
        ...

    @property
    def _args(
            self
    ) -> ty.Tuple[ty.Union[ty.Type[reapy.Take], ty.Type[reapy.Track]]]:
        ...

    def __getitem__(self, key: ty.Union[str, int]) -> Envelope:
        ...

    def __len__(self) -> int:
        ...
