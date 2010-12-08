# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from metafile import Metafile
from network import ArgFactory

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
        for i in item.getContents():
            self.store(i)
        # TODO: Work out how to store items

    def storeAll(self):

    def getFactory(self):

    def getPort(self):

    def destroy(self, item):

    def checkUserCredentials(self, username, passhash):
