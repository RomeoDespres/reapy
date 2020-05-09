"""Define custom errors."""


class DisabledDistAPIError(Exception):

    def __init__(self):
        message = (
            "Can't reach distant API. Please start REAPER, or call "
            "reapy.config.enable_dist_api() from inside REAPER to enable "
            "distant API."
        )
        super().__init__(message)


class DisabledDistAPIWarning(Warning):

    def __init__(self):
        message = (
            "Can't reach distant API. Please start REAPER, or call "
            "reapy.config.enable_dist_api() from inside REAPER to enable "
            "distant API."
        )
        super().__init__(message)


class DisconnectedClientError(Exception):

    def __init__(self):
        message = "Client disconnected. Call self.connect to reconnect."
        super().__init__(message)


class DistError(Exception):

    def __init__(self, tb_string):
        message = (
            "\n\nAn error occurred while running a function inside REAPER. "
            "Traceback was :\n\n{}"
        ).format(tb_string)
        super().__init__(message)


class ExtensionNotFoundError(Exception):

    def __init__(self, extension, url):
        message = (
            "Extension {} is required by this function but is not available. "
            "Please download it from {}."
        ).format(extension, url)
        super().__init__(message)



class InsideREAPERError(Exception):

    pass


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
    Most reapy objects have a ``has_valid_id`` property that allows
    to check for its validity.
    """

    def __init__(self, object):
        self.object = object
        message = (
            "{} has an invalid ID. Common causes of this error "
            "are closing REAPER or deleting the object referred to "
            "by the aforementioned ID. Try checking for "
            "object.has_valid_id`."
        )
        super().__init__(message.format(object))


class OutsideREAPERError(Exception):

    def __init__(self):
        message = "reapy can not be enabled or disabled from outside REAPER"
        super().__init__(message)


class RedoError(Exception):

    def __init__(self):
        message = "Can't redo."
        super().__init__(message)


class UndefinedEnvelopeError(Exception):

    def __init__(self, index, name, chunk_name):
        if index is not None:
            message = "No envelope with index {}".format(index)
        elif name is not None:
            message = "No envelope with name {}".format(name)
        else:
            message = "No envelope with chunk name {}".format(chunk_name)
        super().__init__(message)


class UndefinedExtStateError(Exception):

    def __init__(self, key):
        message = "Undefined extended state for key {}.".format(key)
        super().__init__(message, key)


class UndefinedFXParamError(Exception):

    def __init__(self, fx_name, name):
        message = "No param named \"{}\" for FX \"{}\"".format(
            name, fx_name
        )
        super().__init__(message)


class UndoError(Exception):

    def __init__(self):
        message = "Can't undo."
        super().__init__(message)
