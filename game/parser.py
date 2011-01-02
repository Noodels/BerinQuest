# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon

class Parser:
    def __init__(self, puppet):
        self.puppet = puppet

    def getPuppet(self):
        return self.puppet

    def parseLine(self, line):
        # Line formatting
        line = line.strip()
        
        # Line splitting, supports escape characters?
        command = line.split()

        # Avoid empty lists
        if len(command) == 0:
            return None

        # Call function
        # command[0] should be case insensitive
        try:
            r = getattr(self, "cmd_"+command[0], self.cmd_idiot)(*command)
        except TypeError:
            r = self.cmd_idiot()

        # Wtf is r? It might be useful
        if r == 'QUIT':
            return r
        else:
            return None

    def cmd_idiot(self, *command):
        # Check puppet's exits

        # If exit, go there
        if len(command) == 1 and self.puppet.getLocation() and \
                self.puppet.getLocation().hasExit(command[0]):
            self.cmd_go("go",command[0])
        else:
            self.puppet.display("You are acting like an idiot")

    def cmd_go(self, go, where):
        src = self.puppet.getLocation()
        if src and src.hasExit(where):
            dest = src.getExit(where)
            dest.show(self.puppet.getAttribute('oshort') + ' arrives')
            
            self.puppet.display("You leave to the "+where)
            self.puppet.moveTo(dest)

            src.show(self.puppet.getAttribute('oshort') + \
                    "leaves to the " + where)
        else:
            self.puppet.display("You see no such exit")

    def cmd_look(self, *command):
        if len(command) < 2:
            self.cmd_idiot()
            return

        t = None
        _lhere = self.puppet.getLocation() != None
        if command[2] == 'own':
            command = command[2:]
            if len(command) < 1 or len(command) > 2:
                self.cmd_idiot()
                return None
            _lhere = False
        else:
            command = command[1:]
        if len(command) == 2:
            try:
                n = int(command.pop(1))
            except ValueError:
                self.cmd_idiot()
                return None
            if n < 1:
                self.puppet.display("You can't look into other dimensions")
                return None
        if len(command) != 1:
            self.cmd_idiot()
            return None

        if command[0] == 'medusa':
            self.puppet.display("YOU LOOK INTO THE EYES OF THE MEDUSA")
            self.puppet.emit(self.puppet.getAttribute('oshort') + \
                    " screams and their face melts as they burn to a crisp")
            return 'QUIT'

        if _lhere:
            t = self.puppet.getLocation().getItem(command[0], n)
        if t == None:
            t = self.puppet.getItem(command[0], n)

        if t != None:
            self.puppet.display("You look at the "+t.getAttribute('oshort'))
            t.display(self.puppet.getAttribute('oshort')+" looks at you")
            self.puppet.display(t.getAttribute('odesc'))
        else:
            self.puppet.display("You do not see that here")

    def cmd_quit(self, q):
        self.puppet.display("See medusa for now")

    def cmd_inventory(self, ignoreVal):
        items = self.puppet.getContents()
        t = ", ".join([i.getAttribute('oshort') for i in items])
        self.puppet.display("You have: "+t)
    
    def cmd_say(self, say, *text):
        if len(text) < 1:
            self.cmd_idiot()
            return None
        t = '"' + " ".join(text) + '"'
        self.puppet.display("You say "+t)
        self.puppet.emit(self.puppet.getAttribute('oshort') + \
                " says " + t)

    def cmd_get(self, get, identifier, n=None):
        n = n or "1"
        try:
            n = int(n)
        except ValueError:
            self.cmd_idiot()
            return None
        if n < 1:
            self.puppet.display("Items in other dimensions are not accessible")
            return None
        
        l = self.puppet.getLocation()
        if l:
            i = l.getItem(identifier, n)

            if type(i) == type(self.puppet):
                self.cmd_idiot()
                return None

            if i != None:
                self.puppet.emit(self.puppet.getAttribute('oshort') + \
                        " gets the " + i.getAttribute('oshort'))
                self.puppet.display("You get the "+i.getAttribute('oshort'))
                i.moveTo(self.puppet)
            else:
                self.puppet.display("You do not see that here")
        else:
            self.puppet.display("There are no items in the void")

        return None

    def cmd_drop(self, drop, identifier, n=None):
        n = n or "1"
        try:
            n = int(n)
        except ValueError:
            self.cmd_idiot()
            return None
        if n < 1:
            self.puppet.display("You can't drop such a thing")
            return None
        
        i = self.puppet.getItem(identifier, n)
        if i:
            self.puppet.display("You drop the "+i.getAttribute('oshort'))
            self.puppet.emit(self.puppet.getAttribute('oshort') + \
                    " drops the " + i.getAttribute('oshort') + " here")
            i.moveTo(self.puppet.getLocation())
        else:
            self.puppet.display("You have no such thing")

        return None
