import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject


class AudioAccessor(ReapyObject):

    def __init__(self, id):
        self.id = id

    @property
    def _args(self):
        return self.id,

    def delete(self):
        """Delete audio accessor."""
        RPR.DestroyAudioAccessor(self.id)

    @property
    def end_time(self):
        """
        End time of audio that can be returned from this accessor.

        Return value is in seconds.

        :type: float
        """
        return RPR.GetAudioAccessorEndTime(self.id)

    def get_samples(
        self, start, n_samples_per_channel, n_channels=1, sample_rate=44100
     ):
        """
        Return audio samples.

        Parameters
        ----------
        start : float
            Start time in seconds.
        n_samples_per_channel : int
            Number of required samples per channel
        n_channels : int, optional
            Number of required channels (default=1).
        sample_rate : float, optional
            Required sample rate (default=44100).

        Returns
        -------
        samples : list
            List of length n_samples*n_channels.

        Examples
        --------
        To separate channels use:
        
        >>> samples = audio_accessor.get_samples(0, 1024, 2)
        >>> first_channel = samples[::2]
        >>> second_channel = samples[1::2]
        """
        buffer = [0]*n_channels*n_samples_per_channel
        samples = RPR.GetAudioAccessorSamples(
            self.id, sample_rate, n_channels, start, n_samples_per_channel,
            buffer
        )[1]
        return samples

    @property
    def has_state_changed(self):
        """
        Whether underlying state has changed.

        :type: bool
        """
        return bool(RPR.AudioAccessorValidateState(self.id))

    def hash(self):
        """
        String that changes only if the underlying samples change.

        :type: str
        """
        return RPR.GetAudioAccessorHash(self.id, "")[1]

    @property
    def start_time(self):
        """
        Start time of audio that can be returned from this accessor.

        Return value is in seconds.

        :type: float
        """
        return RPR.GetAudioAccessorStartTime(self.id)
