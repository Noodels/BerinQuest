import sqlite3, yaml

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

    def __init__ (self, filename):
        object.__init__(self)
        self.conn = sqlite3.connect(filename)
        
        
    def __del__ (self):
        print "woo"
        self.conn.commit()
        self.conn.close()

        
    def drop_tables(self):
        """Drop every table defined in the BerinQuest database."""

        c = self.conn.cursor()
    
        for table_name in DatabaseBackend.tables.keys():
            c.execute(DatabaseBackend.tables[table_name][DatabaseBackend.DROP_SQL])

        self.conn.commit()
        c.close()


    def create_tables(self):
        """Create every table defined in the BerinQuest database, if 
        they do not exist already."""
    
        c = self.conn.cursor()
    
        for table_name in DatabaseBackend.tables.keys():
            c.execute(DatabaseBackend.tables[table_name][DatabaseBackend.CREATE_SQL])
    
        self.conn.commit()
        c.close() 

    
    def populate_tables_from_yaml(self, filename):
        """Fill the BerinQuest database with information extracted from 
        the YAML file at filename."""
    
        stream = file(filename, 'r')
        data = yaml.load(stream)
    
        if 'objects' in data.keys():
            self.populate_objects(data['objects'])
        else:
            print "WARNING: No objects in YAML file"
    
        if 'players' in data.keys():
            self.populate_players(data['players'])
        else:
            print "WARNING: No players in YAML file"
    

    def populate_objects(self, object_tree):
        """Given a YAML dictionary tree object_tree of objects, 
        populate the database with the object information 
        contained within the tree."""
    
        for berinobject in object_tree:
            self.populate_object (berinobject)
        
        self.conn.commit()


    def populate_object(self, berinobject):
        """Insert a BerinObject, given its YAML dictionary tree (berinobject), into the 
        database."""

        c = self.conn.cursor()

        # This is so that objects with no location are properly stored.
        # (TODO: Is this necessary?
    
        if berinobject['locationid'] <= 0:
            berinobject["locationid"] = None
            
            
        # Add an entry into the main table for the berinobject
            
        c.execute('''INSERT INTO objects VALUES (?, ?, ?)''',
                  (berinobject['id'], berinobject['typeid'], berinobject['locationid']))


        # Populate berinobject attributes tree

        if 'attributes' in berinobject.keys():
            for attribute in berinobject['attributes']:
                c.execute('''INSERT INTO object_attributes VALUES (?, ?, ?)''',
                          (berinobject['id'], attribute.keys()[0], attribute[attribute.keys()[0]]))
    
    
    def populate_players(self, player_tree):   
        """Given a YAML dictionary tree player_tree of players, 
        populate the database with the player information contained within the tree."""    

        c = self.conn.cursor()
    
        for player in player_tree:
            c.execute('''INSERT INTO players VALUES (?, ?, ?)''',
                      (player['username'], player['passhash'], player['puppetid']))
        
        self.conn.commit()


def main():
    db = DatabaseBackend('db')

    db.drop_tables()
    db.create_tables()
    db.populate_tables_from_yaml("demo.yaml")
    db.test_sql()

    del db
    
if __name__ == '__main__':
    main ()