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

        # List of IDs storing entries to this object
        self._entries = [ ]

        world.register(self)
    
    def getID(self):
        return self.ident

    def display(self, text):
        pass

    def moveTo(self, newLoc):

    def pushItem(self, newItem):

    def removeItem(self, toRemove):

    def setAttribute(self, attr, value):

    def getAttribute(self, attr):

    def delAttribute(self, attr):

    def getLocation(self):

    def renderExits(self):

    def hasExit(self, exit):

    def addExit(self, exit, destination):
        pass
    
    def delExit(self, exit):
        pass

    def addEntry(self, entry):
        self._entries.append(entry)

    def remEntry(self, entry):
        self._entries.remove(entry)

    def getContents(self):
        return self.contents
    
    def getItem(self, identifier, n=None):
        # Default n = 1, ensure n > 0

    # Display text to all other objects in location
    def emit(self, text):

    # Turn values into strings and ints where possible
    def makeStoreSafe(self, upTree=None):
        upTree = upTree or [ ]
        upTree.append(self)

        # Contents
        c = [ ]
        for item in self.contents:
            item.makeStoreSafe(upTree)
            c.append(item.getID())
        assert len(self.contents) == 0, \
                "Contents were not removed from item upon makeStoreSafe()"
        self.contents = c
        
        # Entries
        for e in [self.world.getByID(i) for i in self._entries]:
            if e != None:
                e.replaceExit(self, self.getID())

        # Location
        if self.loc:
            self.loc.removeItem(self)
            self.loc = self.loc.getID()

    # A non-None value signifies an error
    def returnFromStore(self, upTree=None):
        upTree = upTree or [ ]
        upTree.append(self)

        # Location
        if self.loc:
            l = self.world.getByID(self.loc)
            if l == None:
                # Location not loaded?
                l = self.world.retrieve(self.loc)
                assert l != None, \
                        "Unable to retrieve location for %d"%(self.getID())
            self.loc = None
            self.moveTo(l)

        # Entries
        for e in [self.world.getByID(i) for i in self._entries]:
            if e:
                e.replaceExit(self.getID(), self)

        # Contents
        c = [ ]
        for itemID in self.contents:
            c.append(self.world.retrieve(itemID), upTree)
        self.contents = c
        
        return None

# The Room class, only slightly different to the  Object class
class Room(BerinObject):
    def __init__(self, world, loc, **attribs):
        self.exits = { }
        Object.__init__(self, world, loc, **attribs)

    def renderExits(self):
        return ", ".join(self.exits.keys())
    
    def addExit(self, exit, destination):
        destination.addEntry(self.getID())
        self.exits[exit] = destination

    def hasExit(self, exit):
        return (exit in self.exits.keys())
    
    def delExit(self, exit):
        self.exits[exit].remEntry(self.getID())
        del self.exits[exit]

    def replaceExit(self, preval, postval):
        for k, v in self.exits.iteritems():
            if v == preval:
                self.exits[k] = postval
    
    def makeStoreSafe(self, upTree=None):
        BerinObject.makeStoreSafe(self, upTree)
        
        # Exits
        newE = { }
        for e in self.exits.keys():
            if type(self.exits[e]) != int:
                newE[e] = self.exits[e].getID()
            else:
                newE[e] = self.exits[e]
        self.exits = newE

    def returnFromStore(self, upTree=None):
        BerinObject.returnFromStore(self, upTree)

        # Exits
        for e in self.exits.keys():
            d = self.world.getByID(self.exits[e])
            # Leave IDs that cannot be resolved alone
            if d != None:
                self.exits[e] = d

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

    def makeStoreSafe(self, upTree=None):
        BerinObject.makeStoreSafe(self, upTree)
        assert self.client == None, "Attempted to store an active puppet"
