'''
____________________________________________________________________________
    File:         test_entity.py
    File Created: Wednesday, 19th December 2018 11:11:37 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
from unittest import TestCase
from cn4_instrument_common import EntityDescription, Entity

class Test_Entity(TestCase):

    def test_create_entity_from_description(self):
        desc = EntityDescription('id1', int)
        entity = Entity(desc)
        self.assertEqual(entity.entity_desc, desc)