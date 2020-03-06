import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject


class Send(ReapyObject):

    """Track send.

    Attributes
    ----------
    index : int
        position on the track
    is_muted : bool
    is_phase_flipped : bool
    track_id : str
    type : str
        can be 'send', 'hardware' or 'receive'
    """

    _class_name = "Send"

    def __init__(self, track=None, index=0, track_id=None, type="send"):
        if track_id is None:
            message = "One of `track` or `track_id` must be specified."
            assert track is not None, message
            track_id = track.id
        self.index = index
        self.track_id = track_id
        self.type = type

    def _get_int_type(self):
        types = {
            "hardware": 1,
            "send": 0,
            "receive": -1,
        }
        int_type = types[self.type]
        return int_type

    @property
    def _kwargs(self):
        return {
            "index": self.index,
            "track_id": self.track_id,
            "type": self.type
        }

    def delete(self):
        """
        Delete send.
        """
        RPR.RemoveTrackSend(self.track_id, self._get_int_type(), self.index)

    @reapy.inside_reaper()
    def flip_phase(self):
        """
        Toggle whether phase is flipped.
        """
        self.is_phase_flipped = not self.is_phase_flipped

    def get_info(self, param_name):
        value = RPR.GetTrackSendInfo_Value(
            self.track_id, self._get_int_type(), self.index, param_name
        )
        return value

    @property
    def is_mono(self):
        """
        Whether send is mono or stereo.

        :type: bool
        """
        is_mono = bool(self.get_info("B_MONO"))
        return is_mono

    @is_mono.setter
    def is_mono(self, mono):
        self.set_info("B_MONO", mono)

    @property
    def is_muted(self):
        """
        Whether send is muted.

        :type: bool
        """
        is_muted = bool(self.get_info("B_MUTE"))
        return is_muted

    @is_muted.setter
    def is_muted(self, is_muted):
        """
        Mute or unmute send.

        Parameters
        ----------
        is_muted : bool
            Whether to mute or unmute send.
        """
        self.set_info("B_MUTE", is_muted)

    @property
    def is_phase_flipped(self):
        """
        Whether send phase is flipped (i.e. signal multiplied by -1).

        :type: bool
        """
        is_phase_flipped = bool(self.get_info("B_PHASE"))
        return is_phase_flipped

    @is_phase_flipped.setter
    def is_phase_flipped(self, flipped):
        self.set_info("B_PHASE", flipped)

    def mute(self):
        """
        Mute send.
        """
        self.is_muted = True

    @property
    def pan(self):
        """
        Send pan (from -1=left to 1=right).

        :type: float
        """
        pan = self.get_info("D_PAN")
        return pan

    @pan.setter
    def pan(self, pan):
        """
        Set send pan.

        Parameters
        ----------
        pan : float
            New pan between -1 (left) and 1 (right).
        """
        self.set_info("D_PAN", pan)

    def set_info(self, param_name, value):
        RPR.SetTrackSendInfo_Value(
            self.track_id, self._get_int_type(), self.index, param_name, value
        )

    @property
    def source_track(self):
        """
        Source track.

        :type: Track
        """
        track = reapy.Track(self.track_id)
        return track

    def unmute(self):
        """
        Unmute send.
        """
        self.is_muted = False

    @property
    def volume(self):
        """
        Send volume.

        :type: float
        """
        volume = self.get_info("D_VOL")
        return volume

    @volume.setter
    def volume(self, volume):
        self.set_info("D_VOL", volume)
