import time
from threading import Thread, Timer
from .error import InstrumentTimerError

class InstrumentTimer(Thread):
    """Threaded timer that shall be used by all instrument classes
    for constant values update."""
    def __init__(self):
        self._stopped = True
        self._delay=None
        self._timerThread = None
        self._handler=None
    
    def set_handler(self, handler):
        """Sets handler function used by the timer."""
        if not callable(handler):
            raise InstrumentTimerError("Parameter must be function.")
        self._handler = handler

    def set_delay(self, time):
        """Sets time delay used by the timer."""
        if not isinstance(time, float):
            raise InstrumentTimerError("Parameter must be float type.")
        self._delay = time

    def start(self):
        """Starts timer."""
        handler = self._handler
        if not handler:
            raise InstrumentTimerError('No handler specified.')
        delay = self._delay
        if not delay:
            raise InstrumentTimerError('No delay specified.')
        timerThread = Timer(delay, self._internal_handler, [handler]) 
        _timerThread=timerThread
        self._stopped=False
        timerThread.start()

    def _internal_handler(self, handler_function):
        """Internal handler function."""
        #Stop timer
        if self._stopped:
            return

        next_delay = self._delay
        try:
            start_time = time.time()
            handler_function()
            end_time = time.time()
            #Timespan correction with last execution time
            next_delay = max(self._delay - (start_time - end_time), 0.1)            
        except Exception as err:
            raise InstrumentTimerError('Error in handler function.')

        #Stop timer
        if self._stopped:
            return
        #Check handler
        handler = self._handler
        if not handler:
            raise InstrumentTimerError('No handler specified.')
        #Check time
        delay = self._delay
        if not delay:
            raise InstrumentTimerError('No time specified.')
        timerThread = Timer(delay, self._internal_handler, [handler])
        timerThread.start()

    def stop(self):
        """Stop timer."""
        self._stopped=True
        self._timerThread=None