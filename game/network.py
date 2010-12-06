# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from twisted.conch.telnet import StatefulTelnetProtocol
from twisted.internet.protocol import Factory

class ArgFactory(Factory):
    def __init__(self, *arguments):
        self.args = arguments

    def buildProtocol(self, addr):
        # Build something robust
        return p
    
class UserConnection(StatefulTelnetProtocol):
    def __init__(self, # Something ArgFactory compliant and robust please

    def connectionMade(self):
        # world banner? Initialise stuff here
        self.state = 'User'

    def telnet_User(self, line):
        # Follow the conch telnet protocol demonstration closely
