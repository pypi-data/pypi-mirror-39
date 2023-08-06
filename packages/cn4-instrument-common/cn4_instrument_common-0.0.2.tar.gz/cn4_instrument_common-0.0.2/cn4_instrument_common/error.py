'''
____________________________________________________________________________
    File:         error.py
    File Created: Monday, 17th December 2018 6:18:37 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''


class UnknownEntityException(Exception):
    """Exception is raised if an unknown or unsupported entity is requested."""
    def __init__(self):
        super().__init__('Entity is known.')

class InstrumentDisconnectedException(Exception):
    """Exception is raised if an operation on a disconnected instrument is called."""
    def __init__(self):
        super().__init__('Method cannot be called on disconnected instrument.')

class InstrumentConnectedException(Exception):
    """Exception is raised if an operation on a connected instrument is called."""
    def __init__(self):
        super().__init__('Method cannot be called on connected instrument.')

class InstrumentTimerError(Exception):
    """Error class for raising timer errors."""
    def __init__(self, message):
        super().__init__(message)

class InstrumentDecoratorException(Exception):
    """Exception is raised if an decorator is not used on instrument."""
    def __init__(self):
        super().__init__('Decorator not used on instrument.')