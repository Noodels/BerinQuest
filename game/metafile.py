#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Donal Cahill
import yaml
import os

"""The Metafile stores information about a World like its name, description, the banner which is shown when the World is loaded, etc.
It stores its information in a list called data, and any changes made to data are written to disk at metafilePath"""
class Metafile(yaml.YAMLObject):
    def __init__(self, metafilePath):
        self.metafilePath = metafilePath
        # See if the file exists
        if (os.path.isfile(self.metafilePath)):
            self.f = open(self.metafilePath, 'r')
            # If it's not empty, read from it
            if (len(self.f.read()) != 0):
                self.data = yaml.load(open(self.metafilePath, 'r+w'))
            # If it is empty, make data an empty list
            else:
                self.data = {}
        # The file doesn't exist, so make it, and make data an empty list
        else:
            self.data = {}
            self.f = open(self.metafilePath, 'w')
            self.f.close()
            
    """Add an element to data with tag tag and content content, or update the element with the new content if the tag already exists, and then write to metafilePath to reflect this change"""
    def set(self, tag, content):
        self.data[tag] = content
        self.writeFile()
    
    """Return the content of tag tag"""
    def get(self, tag):
        return self.data[tag]
    
    """Remove an element with the tag tag from data, then write to metafilePath to reflect this change"""
    def remove(self, tag):
        self.data.pop(tag)
        self.writeFile()
        
    """Clear the file at metafilePath and write the elements in data to it"""
    def writeFile(self):
        # Clear the file
        self.f = open(self.metafilePath, 'w')
        for i in self.data:
            self.f.write(i + ': ' + self.data[i]+ '\n')
        self.f.close()
        
    """ Delete the file at metafilePath"""
    def deleteFile(self):
        os.remove(self.metafilePath)