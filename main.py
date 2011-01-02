#!/usr/bin/env python2
# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon
from game.world import World
from twisted.internet import reactor
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        bq = World(sys.argv[1])
    else:
        bq = World('data/bq.meta')

    s = reactor.listenTCP(bq.getPort( ), bq.getFactory( ))
    bq.animate(reactor, s)

    reactor.main( )
