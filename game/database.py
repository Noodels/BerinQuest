# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Matt Windsor

import sqlite3, yaml, unicodedata

class DatabaseBackend (object):

    """An object to facilitate communication between BerinQuest and its 
    database storage."""

    # Indices for tables

    DROP_SQL = 0
    CREATE_SQL = 1
    COLS = 2

    # SQL for dropping and creating tables (in that order), followed by 
    # dictionaries of the columns and their indices.

    tables = {
    "objects" : (
    '''DROP TABLE IF EXISTS objects''',
    '''CREATE TABLE IF NOT EXISTS
    objects
    (
      objectid INTEGER PRIMARY KEY NOT NULL,
      typeid INTEGER NOT NULL,
      locationid INTEGER REFERENCES objects(objectid)
      
    );''',
    {"objectid" : 0,
     "typeid" : 1,
     "locationid" : 2}), 
    
    "object_attributes" : (
    '''DROP TABLE IF EXISTS object_attributes''',
    '''CREATE TABLE IF NOT EXISTS
    object_attributes
    (
      objectid INTEGER REFERENCES objects(objectid),
      key STRING NOT NULL,
      value STRING,
      PRIMARY KEY (objectid, key)
    );''',
    {"objectid" : 0, 
     "key" : 1, 
     "value" : 2}),
    
    "players" : (
    '''DROP TABLE IF EXISTS players''',
    '''CREATE TABLE IF NOT EXISTS
    players
    (
      username STRING NOT NULL PRIMARY KEY,
      passhash STRING NOT NULL,
      puppetid INTEGER NOT NULL REFERENCES objects(objectid)
    );''', 
    {"username" : 0, 
     "passhash" : 1, 
     "puppetid" : 2}),
    
    "room_exits" : (
    '''DROP TABLE IF EXISTS room_exits''',
    '''CREATE TABLE IF NOT EXISTS
    room_exits
    (
      roomid INTEGER NOT NULL REFERENCES objects(objectid),
      direction STRING NOT NULL,
      destinationid INTEGER NOT NULL REFERENCES objects(objectid),
      PRIMARY KEY(roomid, direction)
    );''',
    {"roomid" : 0,
     "direction" : 1, 
     "destinationid" : 2})
    }


    def __init__(self, filename):
        """Creates the DatabaseBackend, opening a database connection."""
        object.__init__(self)
        self.conn = sqlite3.connect(filename)
        
        
    def __del__(self):
        """Destroys the DatabaseBackend. closing the database connection."""
        
        self.conn.commit()
        self.conn.close()


    def toASCII(self, string):
        """Convert a potentially Unicode string to ASCII."""
        
        if (isinstance(string, str) == True):       # Normal string, pass through
            return string
        elif (isinstance(string, unicode) == True): # Unicode string, convert
            return unicodedata.normalize('NFKD', string).encode('ascii', 'replace')
        else:                                       # Not a string
            return "???"
        
    def dropTables(self):
        """Drop every table defined in the BerinQuest database."""

        c = self.conn.cursor()
    
        for table_name in DatabaseBackend.tables.keys():
            c.execute(DatabaseBackend.tables[table_name][DatabaseBackend.DROP_SQL])

        self.conn.commit()
        c.close()


    def createTables(self):
        """Create every table defined in the BerinQuest database, if 
        they do not exist already.
        """
    
        c = self.conn.cursor()
    
        for table_name in DatabaseBackend.tables.keys():
            c.execute(DatabaseBackend.tables[table_name][DatabaseBackend.CREATE_SQL])
    
        self.conn.commit()
        c.close() 

    
    def populateTablesFromYaml(self, filename):
        """Fill the BerinQuest database with information extracted from 
        the YAML file at filename.
        """
    
        stream = file(filename, 'r')
        data = yaml.load(stream)
    
        if 'objects' in data.keys():
            self.populateObjects(data['objects'])
        else:
            print "WARNING: No objects in YAML file"
    
        if 'players' in data.keys():
            self.populatePlayers(data['players'])
        else:
            print "WARNING: No players in YAML file"
    

    def populateObjects(self, object_tree):
        """Given a YAML dictionary tree object_tree of objects, 
        populate the database with the object information 
        contained within the tree.
        """
    
        for berinobject in object_tree:
            self.populateObject (berinobject)
        
        self.conn.commit()


    def populateObject(self, berinobject):
        """Insert a BerinObject, given its YAML dictionary tree (berinobject), into the 
        database.
        """

        c = self.conn.cursor()

        # This is so that objects with no location are properly stored.
        # (TODO: Is this necessary? Shouldn't be, return 0 and make it work
    
        #if berinobject['locationid'] <= 0:
        #    berinobject["locationid"] = None
            
            
        # Add an entry into the main table for the berinobject
            
        c.execute('''INSERT INTO objects VALUES (?, ?, ?)''',
                  (berinobject['id'], berinobject['typeid'], berinobject['locationid']))


        # Populate berinobject attributes tree

        if 'attributes' in berinobject.keys():
            for attribute in berinobject['attributes']:
                c.execute('''INSERT INTO object_attributes VALUES (?, ?, ?)''',
                          (berinobject['id'], attribute.keys()[0], attribute[attribute.keys()[0]]))
                
                
        # Populate berinobject exits tree

        if 'exits' in berinobject.keys():
            for exit in berinobject['exits']:
                c.execute('''INSERT INTO room_exits VALUES (?, ?, ?)''',
                          (berinobject['id'], exit.keys()[0], exit[exit.keys()[0]]))    
    
    
    def populatePlayers(self, player_tree):   
        """Given a YAML dictionary tree player_tree of players, 
        populate the database with the player information contained within the tree.
        """    

        c = self.conn.cursor()
    
        for player in player_tree:
            c.execute('''INSERT INTO players VALUES (?, ?, ?)''',
                      (player['username'], player['passhash'], player['puppetid']))
        
        self.conn.commit()
        
        
    def getItem(self, identity):
        """Get a BerinObject out of the database with identity identity.
        
        This returns either ID, type, location ID and attributes 
        (in that order) if a matching object is found, or 
        None, None, None, None if no matching object was found.
        """

        c = self.conn.cursor()
        
        objectRows = c.execute('''SELECT objects.objectid, objects.typeid, objects.locationid
                               FROM objects
                               WHERE objects.objectid == ?''', (identity,)).fetchall()
        
        if (len(objectRows) == 0):
            return None, None, None, None
        else:
            # Should only be at most one object that matches
            assert (len(objectRows) == 1)
            
            itemID = objectRows[0][0]
            itemType = objectRows[0][1]
            itemLID = objectRows[0][2]
            itemAttribs = {}
        
            # Now get the attributes
        
            for row in c.execute('''SELECT object_attributes.key, object_attributes.value
                                 FROM object_attributes
                                 WHERE object_attributes.objectid = ?''', (itemID,)):
                itemAttribs[row[0]] = row[1]
            
            return itemID, itemType, itemLID, itemAttribs



    def getItems(self):
        """Generate an iterator that yields (itemID, itemType, itemLID, itemAttributes) tuples 
        for each item in the database."""

        c = self.conn.cursor()
        
        for row in c.execute('''SELECT objects.objectid, objects.typeid, objects.locationid
                               FROM objects''').fetchall():
                    
            # Get the attributes using row[0] as object ID
            
            itemAttribs = {}
        
            for arow in c.execute('''SELECT object_attributes.key, object_attributes.value
                                 FROM object_attributes
                                 WHERE object_attributes.objectid = ?''', (row[0],)):
                itemAttribs[self.toASCII(arow[0])] = self.toASCII(arow[1])
            
            # Add the attributes to the end of the row.
            
            yield (row[0], row[1], row[2], itemAttribs)
            
     
    def getChildren(self, locationID):
        """Retrieve a list of all object IDs whose location ID is locationID."""
        
        c = self.conn.cursor()
        
        return [row[0] for row in c.execute('''SELECT objects.objectID
                                            FROM objects
                                            WHERE objects.locationID = ?''', 
                                            (locationID,))]
     
    def storeItem(self, itemID, itemType, itemLID, itemAttribs):
        """Store a BerinObject's data (ID, type, location ID and attribute
        dictionary respectively) into the database."""    

        c = self.conn.cursor()
        
        # Store non-attribute data
        
        c.execute('''INSERT INTO objects
                  VALUES (?, ?, ?)''', 
                  (itemID, itemType, itemLID))
        
        
        # Store attributes
        
        for key in itemAttribs.keys():
            c.execute('''INSERT INTO object_attributes
                      VALUES (?, ?, ?)''',
                      (itemID, key, itemAttribs[key]))
        
        self.conn.commit()
        
        
    def delItem(self, identity, new_location):
        """Strike a BerinObject from of the database with identity identity,
        if it exists in the database.
        
        All items in the database that are located inside this BerinObject 
        will be moved to the location new_location."""       
        
        c = self.conn.cursor()

        # Move objects out of item to be stricken into new location

        c.execute('''UPDATE objects
                  SET locationid = ?
                  WHERE locationid = ?''',
                  (new_location, identity))


        # Delete all data we have on the stricken item

        c.execute('''DELETE
                  FROM objects
                  WHERE objects.objectid = ?''',
                  (identity,))
                  
        c.execute('''DELETE
                  FROM object_attributes
                  WHERE object_attributes.objectid = ?''', 
                  (identity,))
        
        c.execute('''DELETE
                  FROM room_exits
                  WHERE room_exits.roomid = ?
                  OR room_exits.destinationid = ?''',
                  (identity, identity))
        
        self.conn.commit()


    def getUser(self, identity):
        """Retrieve the user with identity identity (this is currently 
        equivalent to their username).
        
        This returns either username, passhash and puppet ID 
        (in that order) if a matching player is found, or 
        None, None, None if no matching player was found.
        """
        
        c = self.conn.cursor()
        
        playerrows = c.execute('''SELECT players.username, players.passhash, players.puppetid
                               FROM players
                               WHERE players.username = ?''', 
                               (identity,)).fetchall()
        
        if (len(playerrows) == 0):
            return None, None, None
        else:
            # Should be only one entry at most for a user!
            assert (len(playerrows) == 1)
            
            username = self.toASCII(playerrows[0][0])
            passhash = self.toASCII(playerrows[0][1])
            puppetID = playerrows[0][2]
            
            return username, passhash, puppetID
        
    
    def storeUser(self, username, passhash, puppetid):
        """Store user credentials into the database."""
        
        c = self.conn.cursor()
        
        c.execute('''INSERT INTO players
                  VALUES (?, ?, ?)''', 
                  (username, passhash, puppetid))
        
        self.conn.commit()
        
        
    def getExits(self, roomid):
        """Get a dictionary of all exits connected to the room with ID roomid."""
        
        c = self.conn.cursor()
        
        exitdict = {}
        
        for row in c.execute('''SELECT room_exits.direction, room_exits.destinationid
                             FROM room_exits
                             WHERE roomid = ?''', 
                             (roomid,)):
            exitdict[self.toASCII(row[0])] = row[1]
            
        return exitdict
    

    def storeExit(self, objectid, direction, destinationid):
        """Store a room exit in the database."""
        
        c = self.conn.cursor()
        
        c.execute('''INSERT INTO room_exits 
                     VALUES (?, ?, ?)''', 
                  (objectid, direction, destinationid))
        
        self.conn.commit()
        
