import unittest
import time
from unittest.mock import MagicMock
from cn4_instrument_common.timer import InstrumentTimer
from cn4_instrument_common.error import InstrumentTimerError

class Test_InstrumentTimer(unittest.TestCase):
    def test_timer_init_besuccessful(self):        
        InstrumentTimer()

    def test_set_handler_raises_error(self):        
        it = InstrumentTimer()
        self.assertRaises(InstrumentTimerError, it.set_handler, "i should be a function")
        it.set_handler(lambda: None)

    def test_set_time_raises_error(self):        
        it = InstrumentTimer()
        self.assertRaises(InstrumentTimerError, it.set_delay, "i should be a time")
        it.set_delay(5.0)

    def test_start_raises_exception(self):
        it = InstrumentTimer()
        #Handler exception
        self.assertRaises(InstrumentTimerError, it.start)
        it.set_handler(lambda: None)
        self.assertRaises(InstrumentTimerError, it.start)
        it.set_delay(0.5)
        it.start()
        it.stop()

    def test_timer_calls_handler(self):
        it = InstrumentTimer()
        method = MagicMock(name="fake_handler")                
        #Handler exception
        cnt = 0
        it.set_handler(method)
        self.assertRaises(InstrumentTimerError, it.start)
        it.set_delay(0.2)
        it.start()        
        time.sleep(0.5)        
        it.stop()
        self.assertEqual(method.call_count, 2)

    def test_timer_stopps(self):
        it = InstrumentTimer()
        method = MagicMock(name="fake_handler")                
        #Handler exception
        cnt = 0
        it.set_handler(method)
        self.assertRaises(InstrumentTimerError, it.start)
        it.set_delay(0.2)
        it.start()        
        time.sleep(0.5)        
        it.stop()
        time.sleep(0.5)
        self.assertTrue(it._stopped)
        self.assertIsNone(it._timerThread)
        self.assertEqual(method.call_count, 2)

if __name__ == '__main__':
    unittest.main()