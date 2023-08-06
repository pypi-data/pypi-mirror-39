class UnknownEntityException(Exception):
    """Exception is raised if an unknown or unsupported entity is requested."""
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class InstrumentDisconnectdException(Exception):
    """Exception is raised if an operation on a disconnected instrument is called."""
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class InstrumentTimerError(Exception):
    """Error class for raising timer errors."""
    def __init__(self, message):
        super().__init__(message)