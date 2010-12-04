class Object:
    def __init__(self, world, loc, **attribs):
        self.ident = world.getNewID()
        self.world = world
        self.loc = loc
        self.attributes = attribs
        self.contents = [ ]

    def display(self, text):
        pass

    def moveTo(self, newLoc):

    def pushItem(self, newItem):

class Room(Object):
    def __init__(self, world, loc, **attribs):
        self.exits = { }
        Object.__init__(self, world, loc, **attribs)

    def renderExits(self):
        return ", ".join(self.exits.keys())

class Puppet(Object):
    def __init__(self, world, loc, **attribs):
        self.client = None
        Object.__init__(self, world, loc, **attribs)

    def display(self, text):
        if self.client != None:
            self.client.sendLine(text)

    def registerClient(self, newClient):

    def deregisterClient(self):
