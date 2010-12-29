#!/usr/bin/env python2
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Donal Cahill, Berin Smaldon
from game.metafile import Metafile
import unittest
from os import path

"""Unit test for Metafile. Tests the creation of a blank Metafile, adding, changing, and removing elements, and deleting the Metafile from disk"""
class MetafileTestCase(unittest.TestCase):
    def setUp(self):
        self.testMetafile = Metafile('test.yaml')
    
    def test_1_init(self):
        # Test that the name element doesn't exist
        self.assertEqual(len(self.testMetafile), 1)
    
    def test_2_add(self):
        # Add name and description elements to the list    
        self.testMetafile['name'] = 'BerinQuest Test World'
        self.testMetafile['description'] = 'An awesome, experimental world!'
        # Check it worked
        self.assertEqual(self.testMetafile['name'],'BerinQuest Test World')
        self.assertEqual(self.testMetafile['description'], 'An awesome, experimental world!')
    
    def test_3_change(self):
        # Change the value of description
        self.testMetafile['description'] = 'A splelling mistake!'
        self.testMetafile['description'] = 'I changed the description.'
        # Check it worked
        self.assertEqual(self.testMetafile['description'], 'I changed the description.')
        
    def test_4_remove(self):
        # Remove the name element
        self.testMetafile['name'] = 'BerinQuest Test World'
        del self.testMetafile['name']
        # Check it worked
        assert 'name' not in self.testMetafile.keys()
    
    def test_5_getNonExistant(self):
        self.assertEqual(self.testMetafile.get("derp"), None)
        
    #def test_6_delete(self):
    #    # Delete the file to clean up
    #    self.testMetafile.deleteFile()
    #    assert not path.isfile('test.yaml')
        
if __name__ == '__main__':
    unittest.main()
