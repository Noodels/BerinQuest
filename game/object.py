class Object:
    def __init__(self, world, loc, **attribs):
        self.ident = world.getNewID()
        self.world = world
        self.loc = loc
        self.attributes = attribs
        self.contents = [ ]
