class DisabledDistAPIError(Exception):
    
    def __init__(self):
        message = (
            "reapy distant API is disabled. Please call "
            "`reapy.config.enable_dist_api()` from inside REAPER."
        )
        super(DisabledDistAPIError, self).__init__(message)


class DisconnectedClientError(Exception):

    def __init__(self):
        message = "Client disconnected. Call self.connect to reconnect."
        super(DisconnectedClientError, self).__init__(message)


class DistError(Exception):
    
    def __init__(self, tb_string):
        message = (
            "\n\nAn error occurred while running a Program in the server. "
            "Traceback was :\n\n{}"
        ).format(tb_string)
        super(DistError, self).__init__(message)
        
class UndefinedExtStateError(Exception):
    
    def __init__(self, key):
        message = "Undefined extended state for key {}.".format(key)
        super(UndefinedExtStateError, self).__init__(message, key)