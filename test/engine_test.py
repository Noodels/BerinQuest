#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.network import ArgFactory, UserConnection
from obj_test import DummyWorld
from unittest import main, TestCase, assertEqual, assertRaises

from twisted.internet import reactor

class NetTestCase(TestCase):
    def setUp(self):
        self.wrld = DummyWorld( )
        self.factoryOne = ArgFactory(wrld, 4, 12)
        self.factoryTwo = ArgFactory(wrld)

        self.factoryOne.protocol = UserConnection
        self.factoryTwo.protocol = UserConnection

    def test_argumentPassing(self):
        assertEqual(self.factoryOne.getWorld( ), self.wrld)
        assertEqual(self.factoryTwo.getWorld( ), self.wrld)

        assertEqual(self.factoryOne.getArg(0), 4)
        assertEqual(self.factoryOne.getArg(1), 12)
        assertRaises(IndexError, self.factoryOne.getArg, 2)
        assertRaises(IndexError, self.factoryTwo.getArg, 0)
        reactor.stop()

    # Unsure of how to implement further testing on an event driven framework
    # Suggestions welcome
    # TODO: Implement more network testing
    # more network testing available in custom_testrig.py

if __name__ == '__main__':
    reactor.callLater(1, main)
    reactor.run()
