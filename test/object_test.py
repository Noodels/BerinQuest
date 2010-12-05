#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game import world
from game import objects
import unittest
import re

class DummyClient:
    def __init__(self):
        self.data = ""

    def sendLine(self, line):
        self.data += line

class ObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.mywld = world.World( )
        self.a = objects.Room(mywld, None, ishort="A blank room")
        self.b = objects.Room(mywld, None, ishort="A room with a window")
        
        self.b.addExit("north", self.a)
        self.a.addExit("south", self.b)

        self.c = objects.Object(mywld, self.a, oshort="a projector",
                odesc="The projector projects the words \"I <3 Runciman\" onto a wall.")
        self.d = objects.Object(mywld, self.b, oshort="toast",
                odesc="A cold slice of toast has been abandoned here.")
        self.e = objects.Object(mywld, self.a, oshort="a bag",
                odesc="A bag woven from the stuff of 26 different programming languages.")
        self.f = objects.Puppet(mywld, self.b, oshort="Berin",
                odesc="He is on a quest.")
        self.f.client = DummyClient()
    
    def test_render(self):
        self.f.cmd_look(["look"])
        unittest.assertTrue(re.compile("toast").match(self.f.client.data))
        unittest.assertTrue(re.compile("north").match(self.f.client.data))
        self.f.client.data = ""

        self.f.moveTo(self.a)
        self.f.cmd_look(["look"])
        unittest.assertTrue(re.compile("projector").match(self.f.client.data))
        unittest.assertTrue(re.compile("bag").match(self.f.client.data))
        unittest.assertTrue(re.compile("south").match(self.f.client.data))

        self.f.client.data = ""
        self.f.cmd_look(["look", "projector"])
        unittest.assertTrue(re.compile("Runciman").match(self.f.client.data))

        self.f.client.data = ""
        self.f.cmd_look(["look", "toast"])
        unittest.assertTrue(re.compile("abandoned").match(self.f.client.data) == None)

    def test_location(self):
        self.f.moveTo(self.a)
        unittest.assertTrue(self.f     in self.a.contents)
        unittest.assertTrue(self.f not in self.b.contents)

        self.moveTo(self.b)
        unittest.assertTrue(self.f not in self.a.contents)
        unittest.assertTrue(self.f     in self.b.contents)

    def test_inventory(self):
        self.c.moveTo(self.e)
        unittest.assertTrue(self.c in self.e.contents)

        self.e.moveTo(self.f)
        unittest.assertTrue(self.e in self.f.contents)

        self.f.client_data = ""
        self.f.cmd_inventory(["inventory"])
        unittest.assertTrue(re.compile("bag").match(self.f.client.data))

if __name__ == '__main__':
    unittest.main()
