# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from metafile import Metafile
from network import ArgFactory
from objects import BerinObject, Room, Puppet, itemTypes
from database import DatabaseBackend
import pickle

class DestroyerRoom:
    def __init__(self, world):
        self.world = world
    def pushItem(self, item):
        for i in item.getContents():
            i.moveTo(self)
        self.world.strikeFromDatabase(item.getID())
        self.world.deregisterItem(item)

# World class, defines each world
class World:
    def __init__(self, metafilePath):
        self.defaultAttributes = { }
        self.objects = [ ]
        self.rooms = [ ]
        self.puppets = [ ]
        self.latestID = None
        self.destroyer = DestroyerRoom(self)

        self.connections = [ ]
        self.factory = ArgFactory(self)
        self.port = None

        self.reactorRef = None
        self.callCanceller = [ ]

        # Populate default attributes
        
        self.meta = Metafile(metafilePath)

        self.port = self.meta.get("port") or 4242
        self.latestID = self.meta.get("latestID") or 0
        self.tickTime = self.meta.get("ticktime") or 10
        self.db = DatabaseBackend(self.meta.get("dbpath")) or "berin.db"
        self.startingRoom = self.getByID(self.meta.get("spawn"))
        assert self.startingRoom
    
    def __del__(self):
        del self.db
    
    def getByID(self, identity):
        for o in self.objects:
            if o.getID() == identity:
                return o
        return None

    def getNewID(self):
        self.latestID += 1
        return self.latestID

    def register(self, obj):
        objects.append(obj)
        if type(obj) == Room:
            self.rooms.append(obj)
        if type(obj) == Puppet:
            self.puppets.append(obj)

    def deregister(self, obj):
        self.objects.remove(obj)
        self.rooms.remove(obj)
        self.puppets.remove(obj)

    def registerConnection(self, conn):
        self.connections.append(conn)

    def deregisterConnection(self, conn):
        self.connections.remove(conn)

    def getDefaultAttr(self, attr):
        return self.defaultAttributes.get(attr)

    def animate(self, reactor):
        self.reactorRef = reactor
        self.callLater(self.tickTime, self.dummyTick)

    # Use me
    def dummyTick(self):
        self.callLater(self.tickTime, self.dummyTick)
    
    def callLater(self, time, fn, *args):
        if self.reactorRef:
            self.callCanceller.append(
                    self.reactorRef.callLater(time, fn, *args) )

    def freeze(self):
        for i in self.callCanceller:
            i.cancel()
        # TODO: Error handling
        # TODO: Work out how to drop connections and stop listening

    def retrieve(self, identity):
        # Also restore an items contents to that item
        # Database query searching for specified location given by identity?
        # Get itemID, itemType, itemLID, itemAttribs
        
        itemID, itemType, itemLID, itemAttribs = self.db.getItem(identity)

        itemAttribs['id'] = itemID
        item = itemTypes[itemType](self, self.getByID(itemLID), **itemAttribs)
        if item.getLocation == None and itemLID > 0:
            # Item should have a location but doesn't, should only happen
            # when players pick up other players, which shouldn't really
            # happen. Move the item to a safe room.
            item.moveTo(self.startingRoom)

    # Put the exits in rooms right
    def retrRooms(self):
        for r in self.rooms:
            for exit, dest in r.exits.items():
                d = self.getByID(dest)
                assert d
                r.exits[exit] = d
    
    def store(self, item):
        """Store an item in the database."""
        
        itemID = item.getID()
        itemLID = 0

        if type(item) == Room:
            # Cannot store unless exits are made safe
            if Room in [type(d) for d in item.exits.itervalues()]:
                # In this case, the room is probably being stored recursively
                # and should remain persistent to maintain the room network
                if item.getLocation() != None:
                    item._REAL_LOC = item.getLocation().getID()
                    item.moveTo(None)
                return
            else:
                # Store it exits in the Exits table
                if getattr(item, '_REAL_LOC', False):
                    itemLID = item._REAL_LOC

                for exit, dest in item.exits.items():
                    self.db.storeExit(item.getID(), exit, dest)

        itemType = itemTypes.index(type(item))
        
        if itemLID < 1 and item.getLocation() != None:
            itemLID = item.getLocation().getID()
            item.getLocation.removeItem(item)

        for i in item.getContents():
            self.store(i)

        self.db.storeItem (itemID, itemType, itemLID, item.attributes)

    def storeIfNCli(self, puppet):
        if puppet.client == None:
            self.store(puppet)

    def storeAll(self):
        for r in self.rooms:
            for exit, dest in r.exits:
                r.exits[exit] = dest.getID()

        while len(self.objects) > 0:
            self.store(self.objects[0])

    def getFactory(self):
        return self.factory

    def getPort(self):
        return self.port

    def destroy(self, item):
        if type(item) != Puppet:
            item.moveTo(self.destroyer)

    def checkUserCredentials(self, username, passhash):
        """Check to see if the user details given match with the 
        user records in the database."""
        
        chkUsername, chkPasshash, chkPuppetID = self.db.getUser (username)
        
        if (chkUsername == username
            and chkPasshash == passhash):
            return True
        else:
            return False
        