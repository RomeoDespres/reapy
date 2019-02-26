import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program


class Take(ReapyObject):

    _class_name = "Take"

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    @property
    def _args(self):
        return (self.id,)

    def add_fx(self, name, even_if_exists=True):
        """
        Add FX to track and return it.

        Parameters
        ----------
        name : str
            FX name.
        even_if_exists : bool, optional
            Whether the FX should be added even if there already is an
            instance of the same FX on the track (default=True).

        Returns
        -------
        fx : FX
            New FX on take (or previously existing instance of FX if
            even_if_exists=False).

        Raises
        ------
        ValueError
            If there is no FX with the specified name.
        """
        index = RPR.TakeFX_AddByName(
            self.id, name, 1 - 2*even_if_exists
        )
        if index == -1:
            raise ValueError("Can't find FX named {}".format(name))
        fx = reapy.FX(self, index)
        return fx

    @property
    def fxs(self):
        """
        FXs on take.

        :type: FXList
        """
        return reapy.FXList(self)

    def get_info_value(self, param_name):
        return RPR.GettakeInfo_Value(self.id, param_name)

    @property
    def is_active(self):
        """
        Whether take is active.

        :type: bool
        """
        code = """
        from reapy.core.item.take import Take
        take = Take(take_id)
        is_active = take == take.item.active_take
        """
        return Program(code, "is_active").run(take_id=self.id)[0]

    @property
    def item(self):
        """
        Parent item.

        :type: Item
        """
        return reapy.Item(RPR.GetMediaItemTake_Item(self.id))

    def make_active_take(self):
        """
        Make take active.
        """
        RPR.SetActiveTake(self.id)

    @property
    def n_envelopes(self):
        """
        Number of envelopes on take.

        :type: int
        """
        return RPR.CountTakeEnvelopes(self.id)

    @property
    def n_fxs(self):
        """
        Number of FXs on take.

        :type: int
        """
        return RPR.TakeFX_GetCount(self.id)

    @property
    def source(self):
        """
        Take source.

        :type: Source
        """
        return reapy.Source(RPR.GetMediaItemTake_Source(self.id))

    @property
    def start_offset(self):
        """
        Start time of the take relative to start of source file.

        :type: float
        """
        return self.get_info_value("D_STARTOFFS")

    @property
    def track(self):
        """
        Parent track of take.

        :type: Track
        """
        track_id = RPR.GetMediaItemTake_Track(self.id)
        return reapy.Track(track_id)
