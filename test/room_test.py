# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.objects import Room, BerinObject
from obj_test import DummyWorld
import unittest

class RoomTesting(unittest.TestCase):
    def setUp(self):
        self.world = DummyWorld()
        self.r = Room(self.world, None, ishort="An empty room")
        self.o = BerinObject(self.world, self.r, oshort="a bacon sandwich")

    def test_addExit(self):
        self.r.addExit("vortex", self.r)
        self.o.addExit("out", self.r)

    def test_checkExit(self):
        self.r.addExit("vortex", self.r)
        self.o.addExit("out", self.r)
        self.assertTrue(self.r.hasExit("vortex"))
        self.assertFalse(self.r.hasExit("north"))
        self.assertFalse(self.o.hasExit("out"))

        self.assertEquals(self.r.getExit("vortex"), self.r)

    def test_location(self):
        self.assertEquals(self.o.getLocation(), self.r)

if __name__ == '__main__':
    unittest.main()
