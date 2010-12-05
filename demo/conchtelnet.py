#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from twisted.conch import telnet
from twisted.internet.protocol import Factory
from twisted.internet import reactor

# This implementation implements telnet.StatefulTelnetProtocol
# in a way that suggests how a login system might be
# implemented in the propper program.
class UserConnection(telnet.StatefulTelnetProtocol):
    def connectionMade(self):
        self.sendLine("Welcome to the BerinQuest login prototype!")
        self.transport.write("Username: ")
        self.state = 'User'

    def telnet_User(self, line):
        self.username = line.strip()
        self.transport.write("Password: ")
        # telnet_* commands in StatefulTelnetProtocol return a
        # string indicating which telnet_* command will be
        # run next.
        return 'Password'

    def telnet_Password(self, line):
        if self.username == "Berin" and line.strip() == "quest":
            self.sendLine("Welcome to BerinQuest!")
            return 'Command'
        else:
            # Delay optional
            self.sendLine("Invalid username or password")
            reactor.callLater(3, self._recoverInvalidPswd)
            return 'Discard'

    def _recoverInvalidPswd(self):
        self.transport.write("Username: ")
        self.state = 'User'

    def telnet_Command(self, line):
        line = line.strip()
        if line == "quit":
            self.sendLine("Thankyou for playing!")
            self.transport.loseConnection( )
        else:
            self.sendLine("Command not understood")
            return 'Command'

factory = Factory( )
factory.protocol = UserConnection

reactor.listenTCP(4242, factory)
reactor.run()
