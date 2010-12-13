#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
import unittest
from game.parser import Parser

class DummyPuppet:
    def __init__(self):
        self.connection = None

    def sendLine(self, line):
        if self.connection:
            self.connection.sendLine(line)

    def getLocation(self):
        return None
    
    def getContents(self):
        return []

class DummyConnection:
    def __init__(self):
        self.parser = Parser(DummyPuppet( ))
        self.data = ""
        self.parser.getPuppet().connection = self

    def sendLine(self, line):
        self.data = self.data + line

    def recvLine(self, line):
        return self.parser.parseLine(line)

class ParserTester(unittest.TestCase):
    def setUp(self):
        self.dconn = DummyConnection( )

    def test_flow(self):
        self.assertEquals(self.dconn.recvLine("idiot"), None)
        self.assertEquals(self.dconn.data, "You are acting like an idiot")

if __name__ == '__main__':
    unittest.main()
