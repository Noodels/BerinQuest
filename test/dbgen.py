#!/usr/bin/env python2
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Matt Windsor'''

# dbgen: generates new database from YAML file

from game.database import DatabaseBackend

if __name__ == '__main__':
    dbname = raw_input("Name of new database > ")
    yamlname = raw_input("Name of YAML file to populate from > ")
    
    db = DatabaseBackend(dbname)
    
    print "Cleansing database... ",
    
    db.dropTables()
    
    print "done."
    
    print "Creating tables... ",
    
    db.createTables()
    
    print "done."
    
    print "Populating tables from YAML... ",
    
    db.populateTablesFromYaml(yamlname)
    
    print "done."
    
    print "ENJOY YOUR NEW BERINQUEST WORLD"