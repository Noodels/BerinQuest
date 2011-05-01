##!/usr/bin/env python2
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Donal Cahill, Berin Smaldon
import yaml

class Metafile(dict):
    def __init__(self, pathToYAML):
        self.pathToYAML = pathToYAML
        self.writable = False
        fi = open(pathToYAML, "r")
        super(Metafile, self).__init__(yaml.load(fi.read()) or {})
        fi.close()

    # Typically, the metafile might ought to be readonly
    def setWritable(self, writable=True):
        self.writable = writable

    def __del__(self):
        if self.pathToYAML and self.writable:
            fi = open(self.pathToYAML, "w")
            yaml.dump(dict(self), fi)
            fi.close()
