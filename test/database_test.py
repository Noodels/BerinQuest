# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Matt Windsor

import unittest
from game.database import DatabaseBackend
from game.objects import itemTypes
import game.objects

class DatabaseTesting(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseBackend ('berin.db')
        self.db.dropTables()
        self.db.createTables()

    def tearDown(self):
        del self.db


    def testYamlParse(self):
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()