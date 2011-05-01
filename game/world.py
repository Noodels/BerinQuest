# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon, Matt Windsor
from metafile import Metafile
from network import ArgFactory, UserConnection
from objects import BerinObject, Room, Puppet, itemTypes
from database import DatabaseBackend
import pickle

# World class, defines each world
class World:
    def __init__(self, metafilePath):
        self.defaultAttributes = { }
        self.objects = [ ]
        self.rooms = [ ]
        self.puppets = [ ]
        self.latestID = None

        self.connections = [ ]
        self.factory = ArgFactory(self)
        self.factory.protocol = UserConnection
        self.port = None

        self.reactorRef = None
        self.callCanceller = [ ]

        # Populate default attributes
        # TODO: Get default attributes
        
        self.meta = Metafile(metafilePath)

        self.port = int(self.meta.get("port")) or 4242
        assert type(self.port) == int
        #self.latestID = self.meta.get("latestID") or 0
        self.tickTime = self.meta.get("ticktime") or 10
        assert type(self.tickTime) == int
        dbpath = self.meta.get("dbpath") or "berin.db"
        assert type(dbpath) == str
        # Starting room is in ID form
        self.startingRoom = self.meta.get("spawn")
        assert self.startingRoom

        self.db = DatabaseBackend(dbpath)
        self.latestID = 0
        
        self.retrieveALL()

        # Set locations
        self.finalizeRetrieval()
        # Set exits correctly
        self.retrRooms()

        # Remove puppets
        for p in self.puppets:
            self.store(p)
            self.puppets.remove(p)
            self.objects.remove(p)

        self.startingRoom = self.getByID(self.startingRoom)
        assert self.startingRoom != None

    def __del__(self):
        del self.db
        del self.meta
    
    def getByID(self, identity):
        for o in self.objects:
            if o.getID() == identity:
                return o
        return None

    def getNewID(self):
        self.latestID += 1
        self.meta.set("latestID", self.latestID)
        return self.latestID

    def register(self, obj):
        self.objects.append(obj)
        #if type(obj) == Room:
        #    self.rooms.append(obj)
        #if type(obj) == Puppet:
        #    self.puppets.append(obj)

    def registerRoom(self, r):
        self.rooms.append(r)

    def registerPuppet(self, p):
        self.puppets.append(p)

    def deregister(self, obj):
        self.objects.remove(obj)
        self.rooms.remove(obj)
        self.puppets.remove(obj)

    def registerConnection(self, conn):
        self.connections.append(conn)

    def deregisterConnection(self, conn):
        self.connections.remove(conn)

    def getDefaultAttr(self, attr):
        return self.defaultAttributes.get(attr, None)

    def animate(self, reactor, factoryStopper):
        self.stop = factoryStopper
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
        self.stop.stopListening()

        for c in self.connections:
            c._quitFlag = 1
            c.transport.loseConnection()
    
    # Retrieves an item from the database and returns it
    def retrieve(self, itemID):
        iDetails = self.db.getItem(itemID)
        if iDetails[0] == None:
            return None
        else:
            item = self.createItem(*iDetails)
            locID = getattr(item, '_REAL_LOC')
            loc = self.getByID(locID)
            if loc != None:
                item.moveTo(loc)
            else:
                item.moveTo(self.startingRoom)
            return item

    def retrieveALL(self):
        """Retrieve all items from the database backend.
        
        This also appropriately sets latestID to the highest ID 
        present in the database.
        """
        
        # getItems is an iterator retrieving tuples
        # (itemID, itemType, itemLocationID, itemAttributes)
        
        for i in self.db.getItems():
            self.latestID = max(self.latestID, i[0])
            self.createItem (i[0], i[1], i[2], i[3])


    def createItem(self, itemID, itemType, itemLID, itemAttribs):
        """Create a new item in memory given the item's ID, type, location ID
        and attributes, as retrieved for example from the database.
        """

        itemAttribs['id'] = itemID

        # NOTE: The item location can't be retrieved yet as it may not have 
        # been pulled out of the database yet.  We'll resolve it later but, 
        # for now, give it the LID as param _REAL_LOC.
        # TODO: clean this up?
        
        item = itemTypes[itemType](self, None, **itemAttribs)
        item._REAL_LOC = itemLID
        
        #if item.getLocation == None and itemLID > 0:
            # Item should have a location but doesn't, should only happen
            # when players pick up other players, which shouldn't really
            # happen. Move the item to a safe room. Might be game start.
        #    item.moveTo(self.startingRoom)
        #    item._REAL_LOC = itemLID

        # v-- Not necessary (all items retrieved)
        # Get all objects whose LID is this object's ID
        #for childID in self.db.getChildren(itemID):
        #    self.retrieve(childID)

        if itemTypes[itemType] == Room:
            item.setExits(self.db.getExits(itemID))

        return item
    
    def finalizeRetrieval(self):
        for o in self.objects:
            i = getattr(o, "_REAL_LOC", False)
            if i:
                d = self.getByID(i)
                o.moveTo(d)
                del o._REAL_LOC
            else:
                assert type(o.getLocation()) != int, "Room location set as integer"
            

    # Put the exits in rooms right
    def retrRooms(self):
        print "Finalising",len(self.rooms),"rooms"
        for r in self.rooms:
            for exit, dest in r.exits.items():
                d = self.getByID(dest)
                assert d
                assert type(d) != int, "Room exit set as integer"
                r.exits[exit] = d
                #print "DEBUG: Set exit of", r.getAttr('ishort'), "named", exit, "to", d

    def store(self, item):
        """Store an item in the database."""
        
        itemID = item.getID()
        itemLID = 0
        itemType = itemTypes.index(item.__class__)

        if itemType == Room:
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
        
        if itemLID < 1 and item.getLocation() != None:
            itemLID = item.getLocation().getID()
            item.getLocation().removeItem(item)

        for i in item.getContents():
            self.store(i)

        self.db.storeItem (itemID, itemType, itemLID,
                item.getAllAttributes() )

    def storeIfNCli(self, puppet):
        if puppet.client == None:
            self.store(puppet)

    def storeAll(self):
        for r in self.rooms:
            for exit, dest in r.exits:
                r.exits[exit] = dest.getID()

        while len(self.objects) > 0:
            self.store(self.objects[0])

    def strikeFromDatabase(self, itemID):
        if self.getByID(itemID) is not None:
            location = self.getByID(itemID).getLocation()
            
            if location is None:
                location = 0
                
            db.delItem(itemID, self.getByID(itemID).getLocation());

    def getFactory(self):
        return self.factory

    def getPort(self):
        return self.port
    
    def getBanner(self):
        return self.meta.get('banner', "")

    def destroy(self, item):
        item.moveTo(None)
        for c in item.contents:
            self.destroy(c)
        self.deregister(item)
        self.strikeFromDatabase(item.getID())

    def checkUserCredentials(self, username, passhash):
        """Check to see if the user details given match with the 
        user records in the database."""
        
        chkUsername, chkPasshash, chkPuppetID = self.db.getUser (username)
        
        if (chkUsername == username
            and chkPasshash == passhash):
            return chkPuppetID
        else:
            return None
