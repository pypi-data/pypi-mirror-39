'''
____________________________________________________________________________
    File:         test_decorator.py
    File Created: Monday, 17th December 2018 7:21:17 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
import unittest
from cn4_instrument_common.decorator import instrument_connected, instrument_disconnected
from cn4_instrument_common.error import InstrumentDisconnectedException, InstrumentConnectedException

class testclass:
    @instrument_connected
    def func4test(self):
        pass

class testclass_connected:
    connected=True
    @instrument_connected
    def func4test(self):
        pass        

    def is_connected(self):
        return self.connected

class testclass_disconnected:
    connected=False
    @instrument_disconnected
    def func4test(self):
        pass       

    def is_connected(self):
        return self.connected 

class Test_InstrumentConnectedDecorator(unittest.TestCase):
    def test_exception_if_not_InstrumentInterfaceBase(self):
        tc = testclass()
        self.assertRaises(AttributeError, tc.func4test)

    def test_if_connected(self):
        tc = testclass_connected()
        tc.func4test()
        self.assertTrue(True)

    def test_if_disconnected(self):
        tc = testclass_connected()
        tc.connected = False
        self.assertRaises(InstrumentDisconnectedException, tc.func4test)

class Test_InstrumentDisconnectedDecorator(unittest.TestCase):
    def test_exception_if_not_InstrumentInterfaceBase(self):
        tc = testclass()
        self.assertRaises(AttributeError, tc.func4test)

    def test_if_connected(self):
        tc = testclass_disconnected()
        tc.connected=True
        self.assertRaises(InstrumentConnectedException, tc.func4test)

    def test_if_disconnected(self):
        tc = testclass_disconnected()
        tc.func4test()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main(exit=False)