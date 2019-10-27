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


class UndoError(Exception):
    def __init__(self) -> None:
        ...
