from reapy import reascript_api as RPR
import typing as ty


class Source:
    id: str

    def __init__(self, id: str) -> None:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    @property
    def _args(self) -> ty.Tuple[str]:
        ...

    def delete(self) -> None:
        """
        Delete source. Be sure that no references to source remains.
        """
        ...

    @property
    def filename(self) -> str:
        """
        Return source file name.

        Returns
        -------
        filename : str
            Source file name.
        """
        ...

    @property
    def length(self, unit: str = "seconds") -> float:
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
        ...

    @property
    def n_channels(self) -> int:
        """
        Return number of channels in source media.

        Returns
        -------
        n_channels : int
            Number of channels in source media.
        """
        ...

    @property
    def sample_rate(self) -> int:
        """
        Return source sample rate.

        Returns
        -------
        sample_rate : int
            Source sample rate.
        """
        ...

    @property
    def type(self) -> str:
        """
        Return source type ("WAV, "MIDI", etc.).

        Returns
        -------
        type : str
            Source type.
        """
        ...
