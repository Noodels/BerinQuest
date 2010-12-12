# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Matt Windsor

import unittest
from game.database import DatabaseBackend
from game.objects import itemTypes
import game.objects

class DatabaseTesting(unittest.TestCase):
    """A test construct for the database backend system."""

    def setUp(self):
        """Initialise the database construct."""
        
        self.db = DatabaseBackend ('berin.db')
        self.db.dropTables()
        self.db.createTables()

    def tearDown(self):
        """De-initialise the database construct."""
        
        del self.db


    def testYamlParse(self):
        """Test the YAML population functions of the database backend."""
        
        self.db.populateTablesFromYaml('db.yaml')
        
        c = self.db.conn.cursor()
    
        # Test to see if the muniverse object is present
    
        muniverse_object = [row for row in c.execute ('''SELECT object_attributes.objectid
                                                         FROM object_attributes
                                                         WHERE object_attributes.key == 'ishort'
                                                         AND object_attributes.value == 'Muniverse' ''' )]
        self.assertEqual(muniverse_object[0], (2,))
        
        # Now test to see if it's a room
        
        muniverse_type = [row for row in c.execute ('''SELECT objects.typeid
                                                       FROM objects
                                                       WHERE objects.objectid == 2''')]
        self.assertEqual(muniverse_type[0], (itemTypes.index(game.objects.Room),))
    
    
        # Next, get all the objects directly in the muniverse. There should be three
        # (Colin Runciman, Turbo Pascal and a breakfast). 
    
        objects_in_muniverse = [row for row in c.execute('''SELECT object_attributes.value
                                                         FROM object_attributes
                                                         INNER JOIN objects
                                                         ON objects.objectid == object_attributes.objectid
                                                         WHERE object_attributes.key == 'oshort' 
                                                         AND objects.locationid == 2''')]
        self.assertEqual(objects_in_muniverse, [("Colin Runciman",), ("Turbo Pascal",), ("Breakfast",)])
        
        
        # Finally, get all the puppets linked to players.
        
        playermaps = [row for row in c.execute('''SELECT object_attributes.value, players.username, objects.typeid
                               FROM object_attributes
                               INNER JOIN players
                               ON players.puppetid == object_attributes.objectid   
                               INNER JOIN objects
                               ON objects.objectid == object_attributes.objectid
                               WHERE object_attributes.key == 'oshort' ''')]
    
    
        # The matchings should be Colin Runciman -> Berin, Turbo Pascal -> Pascal
        
        self.assertEqual(playermaps[0][0], "Colin Runciman")
        self.assertEqual(playermaps[0][1], "Berin")
        self.assertEqual(playermaps[1][0], "Turbo Pascal")
        self.assertEqual(playermaps[1][1], "Pascal")
    
        
        # All of the rows should belong to Puppets.
        
        for row in playermaps:
            self.assertEqual(row[2], itemTypes.index(game.objects.Puppet))
    
     
        # All done!
    
        c.close() 


    def testAPIObject(self):
        """Test use of the database backend's API to store and get objects."""
        
        self.db.storeItem(1, 2, 0, {"ishort" : "CSE/270", "idesc": "A computer science lab."})
        
        objectID, typeID, locationID, attribs = self.db.getItem(1)
        
        self.assertEqual(objectID, 1)
        self.assertEqual(typeID, 2)
        self.assertEqual(locationID, 0)
        self.assertEqual(attribs, {"ishort" : "CSE/270", "idesc": "A computer science lab."})


    def testAPIPlayer(self):
        """Test use of the database backend's API to check player credentials."""
        
        c = self.db.conn.cursor()
        
        # Try storing and getting a player. Storage at time of writing is manual-only.
        
        c.execute('''INSERT INTO players
                  VALUES ("Berin", "abc123", 1)''')
        
        self.db.conn.commit()
        
        username, passhash, puppetID = self.db.getUser("Berin")
        
        self.assertEqual(username, "Berin")
        self.assertEqual(passhash, "abc123")
        self.assertEqual(puppetID, 1)


    def testAPIExits(self):
        """Test use of the database backend's API to store and get room exits."""
        
        # First, store two rooms.
        
        self.db.storeItem(1, 2, 0, {"ishort" : "CSE/270", "idesc": "A computer science lab."})
        self.db.storeItem(2, 2, 0, {"ishort" : "CSE 2F", "idesc": "The second-floor corridor of the Computer Science building."})

        # Then make an exit pair.
        
        self.db.storeExit(1, "out", 2)
        self.db.storeExit(2, "in", 1)
        
        # Now check the accessor
        
        roomdict = self.db.getExits(1)
        corrdict = self.db.getExits(2)
        
        self.assertEqual(roomdict, {"out" : 2})
        self.assertEqual(corrdict, {"in"  : 1}) 
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()