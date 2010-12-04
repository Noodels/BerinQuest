#!/usr/bin/python2.7
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class DummyProtocol(Protocol):
    def __init__(self, argument):
        self.message = argument
        #Protocol.__init__(self)

    def connectionMade(self):
        self.transport.write(self.message)
        self.transport.loseConnection()

class ArgumentFactory(Factory):
    def __init__(self, *arguments):
        self.args = arguments
        #Factory.__init__(self)

    def buildProtocol(self, addr):
        # Based on the original twisted buildProtocol code
        p = self.protocol(*self.args)
        p.factory = self
        return p

factory = ArgumentFactory("Hello World!\n")
factory.protocol = DummyProtocol

reactor.listenTCP(8001, factory)
reactor.run()
