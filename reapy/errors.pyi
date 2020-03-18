"""Define custom errors."""

import typing as ty


class DisabledDistAPIError(Exception):
    def __init__(self): ...


class DisabledDistAPIWarning(Warning):
    def __init__(self): ...


class SubclassedWarning(Warning):
    def __init__(self): ...


class DisconnectedClientError(Exception):
    def __init__(self): ...


class DistError(Exception):
    def __init__(self, tb_string: str): ...


class InsideREAPERError(Exception):
    ...


class OutsideREAPERError(Exception):
    ...


class RedoError(Exception):
    ...


class UndefinedEnvelopeError(Exception):
    def __init__(self, index: ty.Optional[int], name: ty.Optional[str],
                 chunk_name: ty.Optional[str]) -> None: ...


class UndefinedExtStateError(Exception):
    def __init__(self, key: object) -> None:
        ...


class UndefinedFXParamError(Exception):
    def __init__(self, fx_name: str, name: str) -> None:
        ...


class UndoError(Exception):
    def __init__(self) -> None:
        ...
