import functools

from reapy.errors import ExtensionNotFoundError


def depends_on_extension(extension, url):
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
    message = "module 'reapy.reascript_api' has no attribute"
    def decorator(f):
        """Indicate dependency of a function to an extension.

        If the extension is not available, an `ExtensionNotFoundError`
        will be raised when calling the decorated function.
        """
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except AttributeError as exc:
                if exc.args[0].startswith(message):
                    raise ExtensionNotFoundError(extension, url)
                else:
                    raise exc
        return wrapped
    return decorator


depends_on_sws = depends_on_extension('SWS', 'www.sws-extension.org')
