import reapy
import reapy.reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


class AudioAccessor(ReapyObject):
    id: bytes

    def __init__(self, id: bytes) -> None:
        ...

    @property
    def _args(self) -> ty.Tuple[bytes]:
        ...

    def delete(self) -> None:
        """Delete audio accessor."""
        ...

    @property
    def end_time(self) -> float:
        """
        End time of audio that can be returned from this accessor.

        Return value is in seconds.

        :type: float
        """
        ...

    def get_samples(self,
                    start: float,
                    n_samples_per_channel: int,
                    n_channels: int = 1,
                    sample_rate: int = 44100) -> ty.List[float]:
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
        ...

    @property
    def has_state_changed(self) -> bool:
        """
        Whether underlying state has changed.

        :type: bool
        """
        ...

    def hash(self) -> str:
        """
        String that changes only if the underlying samples change.

        :type: str
        """
        ...

    @property
    def start_time(self) -> float:
        """
        Start time of audio that can be returned from this accessor.

        Return value is in seconds.

        :type: float
        """
        ...
