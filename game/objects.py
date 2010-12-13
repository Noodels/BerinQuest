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
        pass

    def pushItem(self, newItem):
        pass

    def removeItem(self, toRemove):
        pass

    def setAttribute(self, attr, value):
        """Set the attribute attr to value."""
        
        self.attributes[attr] = value

    def getAttribute(self, attr):
        """Get the attribute attr, or None if it does not exist."""
        
        try:
            return self.attributes[attr]
        except KeyError:
            return None
    
    def getAttributes(self):
        """Get the dictionary of attributes."""
        
        return self.attributes

    def delAttribute(self, attr):
        pass

    def getLocation(self):
        pass

    def renderExits(self):
        pass

    def hasExit(self, exit):
        pass

    def addExit(self, exit, destination):
        pass
    
    def delExit(self, exit):
        pass

    def getContents(self):
        return self.contents
    
    def getItem(self, identifier, n=None):
        pass
        # Default n = 1, ensure n > 0

    # Display text to all other objects in location
    def emit(self, text):
        pass

# The Room class, only slightly different to the  Object class
class Room(BerinObject):
    def __init__(self, world, loc, **attribs):
        self.exits = { }
        Object.__init__(self, world, loc, **attribs)

    def renderExits(self):
        return ", ".join(self.exits.keys())
    
    def addExit(self, exit, destination):
        self.exits[exit] = destination

    def hasExit(self, exit):
        return (exit in self.exits.keys())
    
    def delExit(self, exit):
        del self.exits[exit]

# Objects that represent the players, mostly they just need to be tired to
# an appropriate connection class, but None should be supported for
# link-dead clients.
class Puppet(BerinObject):
    def __init__(self, world, loc, **attribs):
        self.client = None
        self._quitFlag = 0
        Object.__init__(self, world, loc, **attribs)

    def display(self, text):
        if self.client != None:
            self.client.sendLine(text)

    def registerClient(self, newClient):
        pass

    def deregisterClient(self):
        pass

# Item type list, please keep up to date:
itemTypes = [
        BerinObject,
        Room,
        Puppet,
]
