#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
import unittest
from game.world import World
from game.objects import BerinObject

class WorldTester(unittest.TestCase):
    def setUp(self):
        assertRaises(IOError, World, 'doesnotexist.meta')
        self.world = World('wtester.meta')

    def test_basicInit(self):
        o = self.world.getByID(self, 1)
        unittest.assertNotEqual(o, None)

        o = self.world.getByID(self, 14890141)
        unittest.assertEqual(o, None)

    def test_store(self):
        r = self.world.getByID(1)
        o = BerinObject(self.world, r, oshort="umquloaxatl") # no confusion
        i = o.getID()

        o.setAttribute("id", 51421)
        self.world.store(o)

        unittest.assertEquals(r.getItem("umquloaxatl"), None)

        o = self.world.retrieve(i)
        unittest.assertEquals(o.getID(), i)

        o.pushItem(o)
        
        self.world.store(o)
        o = self.world.retrieve(i)
        unittest.assertEquals(o, o.getItem("umquloaxatl"))

        self.o = o

    def test_destroy(self):
        r = self.world.getByID(1)
        b = BerinObject(self.world, r, oshort="doomed object")
        b.moveTo(self.o)
        world.destroy(self.o)
        
        unittest.assertEquals(r.getItem(self.o.getAttribute("oshort")), None)

        unittest.assertEquals(self.world.getByID(self.o.getID()), None)
        unittest.assertEquals(self.world.getByID(b.getID()), None)

        unittest.assertFalse(b in self.o.contents)
        unittest.assertFalse(o in self.o.contents)

if __name__ == '__main__':
    unittest.main()
