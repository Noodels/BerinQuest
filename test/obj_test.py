#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.objects import BerinObject
from unittest import TestCase, assertEquals, assertTrue, main

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

    def test_creation(self):
        a = BerinObject(self.world, None, oshort="Lis0r's wrath",
                odesc="Lis0r's wrath has been condensed into physical form and placed in a jar. The jar is hot.")
        # Initialisation assertions
        assertEquals(a.getLocation( ), None)
        assertEquals(a.getID( ), self.world.latestID)
        self.wrath = a

    def test_moveTo(self):
        b = BerinObject(self.world, None, oshort="a braced steel box",
                odesc="A reinforced box made of 3 inch steel.")
        
        # Moving a into b causes a to be inside b, and b to contain a
        self.wrath.moveTo(b)
        assertEquals(self.wrath.getLocation( ), b)
        assertTrue(self.wrath in b.contents)

        # BerinObject.hasItem( item ) accepts item as an item or item ID
        assertTrue(self.wrath in b.contents)
        assertTrue(b.hasItem(self.wrath))
        assertTrue(b.hasItem(self.wrath.getID( )))

        self.box = b

    def test_moveToSpecifics(self):
        self.wrath.pushItem(self.box)
        assertTrue(self.wrath.hasItem(self.box))
        
        assertTrue(self.box.getLocation != self.wrath)

    def test_moveOut(self):
        self.a.moveTo(None)
        self.b.moveTo(None)

        assertEquals(self.a.loc, None)
        assertEquals(self.b.loc, None)

    def test_idAssignment(self):
        self.c = BerinObject(self.world, None, id=131)
        assertEquals(self.c.ident, 131)

        assertRaises(TypeError, BerinObject, self.world, None, id="bacon")

if __name__ == '__main__':
    main()
