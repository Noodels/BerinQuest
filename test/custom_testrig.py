#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import StatefulTelnetProtocol
from game.world import World
from game import objects

USERNAME = "TestBot"
PASSWORD = "forscience"

class StatefulTestRig(StatefulTelnetProtocol):
    def __init__(self, world):
        self.world = world

    def connectionMade(self):
        print "Connected, awaiting login prompt"
        self.state = 'login'

    def telnet_login(self, line):
        assert (self.world.getBanner( ) + 'Username: ' == line), \
                "Received incorrect banner and/or username statement"
        self.sendLine(USERNAME+"\n")
        print "Received, sending username and awaiting password prompt"
        return 'password'
    
    def telnet_password(self, line):
        assert (line == 'Password: '), \
                "Received incorrect password prompt"
        self.sendLine(PASSWORD+"\n")
        print "Sent, sending password"
        return 'entry'

    def telnet_entry(self, line):
        self.sendLine('say Hello!')
        print "Checking basic command for functionality"
        return 'hello'

    def telnet_hello(self, line):
        assert (line == "You say \"Hello!\"\n"), \
                "Received incorrect response to hello"
        self.sendLine('quit')
        print "Success, closing"
        return 'quit'

    def telnet_quit(self, line):
        assert (line == "Thankyou for playing!\n"), \
                "Received incorrect goodbye message"
        return 'never'

    def telnet_never(self, line):
        raise NeverCallMeError, "Received excess data"
    
    def connectionLost(self):
        assert self.state == 'never', "Premature closure"
        print "Successful transaction with the game world!"
        reactor.stop( )

class TestClientFactory(ClientFactory):
    def __init__(self, world):
        self.world = world

    def startedConnecting(self, connector):
        print "Connecting"

    def buildProtocol(self, addr):
        return StatefulTestRig(self.world)
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost:", reason

    def clientConnectionFailed(self, connector, reason):
        raise ConnectionError, "Could not connect: "+reason

if __name__ == '__main__':
    world = World(None)
    clientFactory = TestClientFactory(world)
    
    reactor.listenTCP(8001, world.getFactory( ))
    reactor.connectTCP('localhost', 8001, clientFactory)
    reactor.run( )
