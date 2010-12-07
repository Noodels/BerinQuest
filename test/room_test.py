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
        unittest.assertTrue(self.r.hasExit("vortex"))
        unittest.assertFalse(self.r.hasExit("north"))
        unittest.assertFalse(self.o.hasExit("out"))

        unittest.assertEquals(self.r.getExit("vortex"), self.r)

if __name__ == '__main__':
    unittest.main()
