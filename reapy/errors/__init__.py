class RedoError(Exception):
    
    def __init__(self):
        message = "Can't redo."
        super(RedoError, self).__init__(message) 
        

class UndefinedEnvelopeError(Exception):
    
    def __init__(self, index, name, chunk_name):
        if index is not None:
            message = "No envelope with index {}".format(index)
        elif name is not None:
            message = "No envelope with name {}".format(name)
        else:
            message = "No envelope with chunk name {}".format(chunk_name)
        super(UndefinedEnvelopeError, self).__init__(message)


class UndoError(Exception):
    
    def __init__(self):
        message = "Can't undo."
        super(UndoError, self).__init__(message)