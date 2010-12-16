#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Donal Cahill
from game.metafile import Metafile
import unittest
from os import path

"""Unit test for Metafile. Tests the creation of a blank Metafile, adding, changing, and removing elements, and deleting the Metafile from disk"""
class MetafileTestCase(unittest.TestCase):
    # Make a global var print1, so it can be used in both test 2 and test 3
    print1 = ""
    def setUp(self):
        self.testMetafile = Metafile('test_banner.yaml')     
        
    def test_1_add(self):
        # Add a nice BerinQuest banner
        self.testMetafile.set('banner', 'BBBBB                 iii          QQQQQ                       tt    \nBB   B    eee  rr rr      nn nnn  QQ   QQ uu   uu   eee   sss  tt    \nBBBBBB  ee   e rrr  r iii nnn  nn QQ   QQ uu   uu ee   e s     tttt  \nBB   BB eeeee  rr     iii nn   nn QQ  QQ  uu   uu eeeee   sss  tt    \nBBBBBB   eeeee rr     iii nn   nn  QQQQ Q  uuuu u  eeeee     s  tttt \n                                                          sss        ')
    def test_2_print(self):
        global print1
        print1 = self.testMetafile.data['banner']
        print print1
    
    def test_3_print_again(self):
        # Make a new Metafile which reads from the same file as the last one
        self.testMetafile2 = Metafile('test_banner.yaml')
        self.print2 = self.testMetafile2.data['banner'] 
        print "\n\n"
        print self.print2
        # Check that what we printed last time and what we printed this time are the same
        self.assertEqual(cmp(print1,self.print2),0)
    
    def test_4_delete(self):
        # Delete the file to clean up
        self.testMetafile.deleteFile()
        assert not path.isfile('test_banner.yaml')
        
if __name__ == '__main__':
    unittest.main()