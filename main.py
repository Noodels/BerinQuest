#!/usr/bin/python2.7
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.world import World
from twisted.internet import reactor

if __name__ == '__main__':
    bq = World('lib/bq.meta')

    reactor.listenTCP(bq.getPort( ), bq.getFactory( ))
    bq.animate(reactor)

    reactor.main( )
