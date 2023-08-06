'''
____________________________________________________________________________
    File:         test_entitydescription.py
    File Created: Wednesday, 19th December 2018 10:46:35 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
from unittest import TestCase
from cn4_instrument_common import EntityDescription

class Test_EntityDescription(TestCase):
    def test_expect_exception_on_none_id(self):
        self.assertRaises(AttributeError, EntityDescription, None, int)

    def test_expect_exception_on_empty_id(self):
        self.assertRaises(AttributeError, EntityDescription, '', int)

    def test_expect_exception_on_none_type(self):
        self.assertRaises(AttributeError, EntityDescription, 'id', None)

    def test_expect_valid_initialisation(self):
        desc = EntityDescription('id', int)
        self.assertTrue(desc.readable)
        self.assertFalse(desc.writable)
        self.assertFalse(desc.internal)

        desc = EntityDescription('id', int, readable = False)
        self.assertFalse(desc.readable)
        self.assertFalse(desc.writable)
        self.assertFalse(desc.internal)

        desc = EntityDescription('id', int, readable = False, writable = True)
        self.assertFalse(desc.readable)
        self.assertTrue(desc.writable)
        self.assertFalse(desc.internal)

        desc = EntityDescription('id', int, readable = False, writable = True, 
            internal = True)
        self.assertFalse(desc.readable)
        self.assertTrue(desc.writable)
        self.assertTrue(desc.internal)
