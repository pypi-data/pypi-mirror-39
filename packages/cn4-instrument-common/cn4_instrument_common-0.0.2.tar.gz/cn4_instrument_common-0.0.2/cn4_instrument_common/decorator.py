'''
____________________________________________________________________________
    File:         decorator.py
    File Created: Monday, 17th December 2018 6:18:16 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
from .error import InstrumentDisconnectedException, InstrumentConnectedException
from functools import wraps

def instrument_connected(func):
    """Decorator checks if instrument is connected and throws exception if not. Use
    on instrument functions, that need connected instrument."""
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            if not args[0].is_connected():
                raise InstrumentDisconnectedException()
            return func(*args, **kwargs)
        except AttributeError as e:
            raise AttributeError('Use this decorator on InstrumentInterfaceBase only')
    return decorator                

def instrument_disconnected(func):
    """Decorator checks if instrument is connected and throws exception if not. Use
    on instrument functions, that need connected instrument."""
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            if args[0].is_connected():
                raise InstrumentConnectedException()
            return func(*args, **kwargs)
        except AttributeError as e:
            raise AttributeError('Use this decorator on InstrumentInterfaceBase only')
    return decorator                
