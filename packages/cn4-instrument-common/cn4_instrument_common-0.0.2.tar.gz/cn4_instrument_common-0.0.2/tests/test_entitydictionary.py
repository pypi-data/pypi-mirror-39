'''
____________________________________________________________________________
    File:         test_entitydictionary.py
    File Created: Monday, 17th December 2018 9:54:23 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
from unittest import TestCase, unittest
from unittest.mock import MagicMock
from cn4_instrument_common.common import EntityDictionary

class Test_EntityDictionary(TestCase):

    def test_add_function(self):
        ed = EntityDictionary()
        self.assertTrue(len(ed)==0)

        on_added_method = MagicMock(name="on_added")  
        on_changed_method = MagicMock(name="on_changed")  
        ed.on_value_added+=on_added_method
        ed.on_value_changed+=on_changed_method
        ed['aaa']=5
        ed['aaa']=6
        self.assertTrue(len(ed)==1)
        self.assertEqual(on_added_method.call_count, 1)
        self.assertEqual(on_changed_method.call_count, 2)

    def test_update_function(self):
        ed = EntityDictionary()
        self.assertTrue(len(ed)==0)

        on_added_method = MagicMock(name="on_added")  
        on_changed_method = MagicMock(name="on_changed")  
        ed.on_value_added+=on_added_method
        ed.on_value_changed+=on_changed_method
        ed['aaa']=5
        ed['aaa']=6
        self.assertTrue(len(ed)==1)
        self.assertEqual(on_added_method.call_count, 1)
        self.assertEqual(on_changed_method.call_count, 2)        

if __name__ == '__main__':
    unittest.main(exit=False)

