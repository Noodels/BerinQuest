# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from metafile import Metafile
from network import ArgFactory
import pickle

# World class, defines each world
class World:
    def __init__(self, metafilePath):
        self.objects = [ ]
        self.rooms = [ ]
        self.puppets = [ ]
        self.latestID = 0

        self.connections = [ ]
        self.factory = ArgFactory(self)

        self.reactorRef = None
        self.callCanceller = [ ]

        # TODO: Load the DB
        self.meta = Metafile(metafilePath)
    
    def getByID(self, identity):

    def register(self, obj):
        objects.append(obj)
        if type(obj) == # TODO: Complete me

    def deregister(self, obj):

    def registerConnection(self, conn):

    def deregisterConnection(self, conn):

    def getDefaultAttr(self, attr):

    def animate(self, reactor):
        self.reactorRef = reactor
        # TODO: Tick function, appends to callCanceller

    # Use me
    def dummyTick(self):
        pass
    
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
    
    def store(self, item):
        # Contents
        c = [ ]
        for i in item.getContents():
            c.append(i.getID())
            self.store(i)
        item.contents = c

        # Location
        item.loc.removeItem(self)
        item.loc = item.loc.getID()

        # Exits
        e = getattr(item, "exits", None)
        if e:
            for k in e.keys():
                if type(item[k]) != int:
                    item[k].setExit(item, item.getID())
                    item[k] = item[k].getID()
        
        # Clients
        assert getattr(item, "client", None) == None, "Stored active puppet"
        
        # World
        del item.world

        # Pickle
        itemID = item.getID()
        itemdata = pickle.dumps(item)

        # Store data into DB
        # TODO: Store item in DB

    def storeAll(self):

    def getFactory(self):

    def getPort(self):

    def destroy(self, item):

    def checkUserCredentials(self, username, passhash):
