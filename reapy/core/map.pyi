import typing as ty


def map(
    function: ty.Callable,
    *iterables: ty.Iterable,
    constants: ty.Mapping[str, ty.Any] = ...,
    kwargs_iterable: ty.Optional[ty.Iterable[ty.Mapping[str, ty.Any]]] = ...
) -> list:
    ...
