import functools
import typing as ty

from reapy.errors import ExtensionNotFoundError

FuncType = ty.Callable[..., ty.Any]
F = ty.TypeVar('F', bound=FuncType)


def depends_on_extension(extension: str, url: str) -> ty.Callable[[F], F]:
    """Return a decorator to indicate dependency to an extension.

    If the extension is not available, an `ExtensionNotFoundError`
    will be raised when calling the decorated function.

    Parameters
    ----------
    extension : str
        Extension name.
    url : str
        URL of the download page or installation instructions of
        the extension.
    """
    ...


depends_on_sws = depends_on_extension('SWS', 'www.sws-extension.org')
