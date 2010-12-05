#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class DummyProtocol(Protocol):
    def __init__(self, argument):
        self.message = argument
        #Protocol.__init__(self)

    def connectionMade(self):
        self.transport.write(self.message)
        self.transport.loseConnection()

# ArgumentFactory takes arguments and passes them onto every one
# of its clients. It is backwards compatible.
class ArgumentFactory(Factory):
    def __init__(self, *arguments):
        self.args = arguments
        # Factory doesn't implement __init__
        #Factory.__init__(self)

    # The source code for Factory was dredged up and modified
    # for this purpose.
    def buildProtocol(self, addr):
        # Based on the original twisted buildProtocol code
        p = self.protocol(*self.args)
        p.factory = self
        return p

factory = ArgumentFactory("Hello World!\n")
factory.protocol = DummyProtocol

reactor.listenTCP(8001, factory)
reactor.run()
