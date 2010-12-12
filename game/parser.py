# Distributed under the terms of the GNU GPLv3
# Copyright 2010 Berin Smaldon

class Parser:
    def __init__(self, puppet):
        self.puppet = puppet

    def parseLine(self, line):
        # Line formatting
        
        # Line splitting, supports escape characters?

        # Avoid empty lists

        # Call function
        # command[0] should be case insensitive
        r = getattr(self, "cmd_"+command[0], self.cmd_idiot)(command)

        # Wtf is r? It might be useful

    def cmd_idiot(self, command):
        # Check puppet's exits

        # If exit, go there
        if condition:
            pass
        else:
            self.puppet.sendLine("You are acting like an idiot")

    def cmd_go(self, command):
        pass

    def cmd_look(self, command):
        pass

    def cmd_quit(self, command):
        pass

    def cmd_inventory(self, command):
        pass
    
    def cmd_say(self, command):
        pass

    def cmd_get(self, command):
        pass

    def cmd_drop(self, command):
        pass
