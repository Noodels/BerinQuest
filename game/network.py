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
        # Note that the telnet protocol should be researched for this,
        # the TelnetProtocol in twisted supports negotiation, use for colour
        # support, this class will filter out colour based on result
        self.state = 'User'

    def sendLine(self, line):
        # Override, perform filters and fall back to original functionality
        StatefulTelnetProtocol.sendLine(self, line)

    def telnet_User(self, line):
        # Follow the conch telnet protocol demonstration closely
