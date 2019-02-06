from reapy import reascript_api as RPR

import wave

class Source:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Source)

    @property
    def data(self):
        if self.type != "WAVE":
            raise NotImplementedError
        file = wave.open(self.filename, "r")
        n_frames = file.getnframes()
        n_channels = file.getnchannels()
        sample_width = file.getsampwidth()
        frames = file.readframes(n_frames)
        file.close()
        scale = 2**(8*sample_width)
        data = [[0. for _ in range(n_channels)] for _ in range(n_frames)]
        for frame in range(n_frames):
            for channel in range(n_channels):
                start = n_channels*sample_width*frame + channel
                b = frames[start:start + sample_width]
                value = int.from_bytes(b, "little", signed=True) / scale
                data[frame][channel] = value
        return data

    @property
    def filename(self):
        """
        Return source file name.

        Returns
        -------
        filename : str
            Source file name.
        """
        _, filename, _ = RPR.GetMediaSourceFileName(self.id, "", 10**5)
        return filename

    @property
    def length(self, unit="seconds"):
        """
        Return source length in `unit`.

        Parameters
        ----------
        unit : {"beats", "seconds"}
            
        Returns
        -------
        length : float
            Source length in `unit`.
        """
        length, _, is_quantized = RPR.GetMediaSourceLength(self.id, 0)
        if is_quantized:
            if unit == "beats":
                return length
            elif unit == "seconds":
                raise NotImplementedError
        else:
            if unit == "beats":
                raise NotImplementedError
            elif unit == "seconds":
                return length

    @property
    def n_channels(self):
        """
        Return number of channels in source media.
        
        Returns
        -------
        n_channels : int
            Number of channels in source media.
        """
        n_channels = RPR.GetMediaSourceNumChannels(self.id)
        return n_channels

    @property
    def sample_rate(self):
        """
        Return source sample rate.

        Returns
        -------
        sample_rate : int
            Source sample rate.
        """
        sample_rate = RPR.GetMediaSourceSampleRate(self.id)
        return sample_rate

    @property
    def type(self):
        """
        Return source type ("WAV, "MIDI", etc.).

        Returns
        -------
        type : str
            Source type.
        """
        _, type, _ = RPR.GetMediaSourceType(self.id, "", 10**5)
        return type
