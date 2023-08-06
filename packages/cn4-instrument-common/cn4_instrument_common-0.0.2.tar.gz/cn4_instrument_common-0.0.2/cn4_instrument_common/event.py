'''
____________________________________________________________________________
    File:         event.py
    File Created: Monday, 17th December 2018 9:11:15 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
class EventHook(object):
    """Simple event handler class, taken from voidspace.org.uk."""
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)