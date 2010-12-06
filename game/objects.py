# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
import re # Use this for getItem

# The Universal Object class
class BerinObject:
    # Mostly define attributes that everything needs to have
    def __init__(self, world, loc, **attribs):
        if 'id' in attribs.keys():
            self.ident = attribs['id']
            del attribs['id'] # Don't store that
        else:
            self.ident = world.getNewID()
        self.world = world
        self.loc = loc
        self.attributes = attribs
        self.contents = [ ]

        world.register(self)
    
    def getID(self):
        return self.ident

    def display(self, text):
        pass

    def moveTo(self, newLoc):

    def pushItem(self, newItem):

    def removeItem(self, toRemove):

    def setAttr(self, attr, value):

    def getAttr(self, attr):

    def delAttr(self, attr):

    def getLocation(self):

    def renderExits(self):

    def hasExit(self, exit):

    def addExit(self, exit):
        pass

    def getContents(self):
        return self.contents
    
    def getItem(self, identifier, n=None):
        # Default n = 1, ensure n > 0

# The Room class, only slightly different to the  Object class
class Room(BerinObject):
    def __init__(self, world, loc, **attribs):
        self.exits = { }
        Object.__init__(self, world, loc, **attribs)

    def renderExits(self):
        return ", ".join(self.exits.keys())

# Objects that represent the players, mostly they just need to be tired to
# an appropriate connection class, but None should be supported for
# link-dead clients.
class Puppet(BerinObject):
    def __init__(self, world, loc, **attribs):
        self.client = None
        Object.__init__(self, world, loc, **attribs)

    def display(self, text):
        if self.client != None:
            self.client.sendLine(text)

    def registerClient(self, newClient):

    def deregisterClient(self):
