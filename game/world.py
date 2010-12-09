# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from metafile import Metafile
from network import ArgFactory
from objects import BerinObject, Room, Puppet
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

        # TODO: Load the DB
        self.meta = Metafile(metafilePath)

        self.port = self.meta.get("port") or 4242
        self.latestID = self.meta.get("latestID") or 0
        self.tickTime = self.meta.get("ticktime") or 10
    
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
        # TODO: Get itemdata from DB
        assert type(itemdata) == str
        item = pickle.loads(itemdata)
        assert item != None

        # World
        item.world = self
        self.register(item)
        errVal = item.returnFromStore()
        while errVal != None:
            # Handle problems

        return item
    
    def store(self, item):
        # Item handles most of its own affairs
        item.makeStoreSafe()
        
        # World
        self.deregister(item)
        del item.world

        # Pickle
        itemID = item.getID()
        itemdata = pickle.dumps(item)

        # Store data into DB
        # TODO: Store item in DB

    def storeIfNCli(self, puppet):
        if puppet.client == None:
            self.store(puppet)

    def storeAll(self):
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
