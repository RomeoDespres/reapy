class OutsideREAPERError(Exception):
    
    def __init__(self):
        message = "reapy can not be enabled or disabled from outside REAPER"
        super(OutsideREAPERError, self).__init__(message)