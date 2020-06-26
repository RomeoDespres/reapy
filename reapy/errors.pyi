"""Define custom errors."""

import typing as ty


class DisabledDistAPIError(Exception):
    ...


class DisabledDistAPIWarning(Warning):
    ...


class DisconnectedClientError(Exception):
    ...


class DistError(Exception):
    ...


class ExtensionNotFoundError(Exception):
    def __init__(self, extension: str, url: str): ...


class InsideREAPERError(Exception):
    ...


class InvalidObjectError(Exception):

    """Raised when an object with invalid ID has tried to access REAPER.

    Common causes of this error are closing REAPER or deleting the
    object referred to by the aforementioned ID.

    The object that caused this error is available as its ``object``
    attribute.

    Parameters
    ----------
    object : ReapyObject
        Object that caused the error.

    Notes
    -----
    Most reapy objects have a ``has_valid_id()`` method that allows
    to check for its validity.
    """

    ...


class OutsideREAPERError(Exception):
    ...


class RedoError(Exception):
    ...


class UndefinedEnvelopeError(Exception):
    def __init__(self, index: ty.Optional[int], name: ty.Optional[str],
                 chunk_name: ty.Optional[str]) -> None:
        ...


class UndefinedExtStateError(Exception):
    def __init__(self, key: object) -> None:
        ...


class UndefinedFXParamError(Exception):
    def __init__(self, fx_name: str, name: str) -> None:
        ...


class UndefinedMarkerError(Exception):

    def __init__(self, index: int): ...


class UndoError(Exception):
    def __init__(self) -> None:
        ...
