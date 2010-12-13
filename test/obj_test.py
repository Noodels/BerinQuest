#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.objects import BerinObject
from unittest import TestCase, main

class DummyWorld:
    def __init__(self):
        self.objs = [ ]
        self.latestID = 0

    def getNewID(self):
        self.latestID += 1
        return self.latestID

    def register(self, obj):
        self.objs.append(obj)

class BerinObjectTester(TestCase):
    def setUp(self):
        self.world = DummyWorld( )
        self.wrath = BerinObject(self.world, None, oshort="Lis0r's wrath",
                odesc="Lis0r's wrath has been condensed into physical form and placed in a jar. The jar is hot.")
        self.box = BerinObject(self.world, None, oshort="a braced steel box",
                odesc="A reinforced box made of 3 inch steel.")

    def test_creation(self):
        a = BerinObject(self.world, None, oshort="an orange",
                odesc="Luckily, the orange is just an object and nothing special.")
        # Initialisation assertions
        self.assertEquals(a.getLocation( ), None)
        self.assertEquals(a.getID( ), self.world.latestID)
        self.assertEquals(a.getLocation( ), a.loc)

    def test_moveTo(self):
        # Moving a into b causes a to be inside b, and b to contain a
        self.wrath.moveTo(self.box)
        self.assertEquals(self.wrath.getLocation(), self.box)
        self.assertTrue(self.wrath in self.box.contents)

        # BerinObject.hasItem( item ) accepts item as an item or item ID
        self.assertTrue(self.box.hasItem(self.wrath))
        self.assertTrue(self.box.hasItem(self.wrath.getID()))

    def test_moveToSpecifics(self):
        self.wrath.pushItem(self.box)
        self.assertTrue(self.wrath.hasItem(self.box))
        
        self.assertTrue(self.box.getLocation() != self.wrath)

    def test_moveOut(self):
        self.wrath.moveTo(None)
        self.box.moveTo(None)

        self.assertEquals(self.wrath.loc, None)
        self.assertEquals(self.box.loc, None)

    def test_idAssignment(self):
        c = BerinObject(self.world, None, id=131)
        self.assertEquals(c.ident, 131)
        self.assertEquals(c.getID(), c.ident)

        self.assertRaises(ValueError, BerinObject, self.world, None, id="bacon")

if __name__ == '__main__':
    main()
