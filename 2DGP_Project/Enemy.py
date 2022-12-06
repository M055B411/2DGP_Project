from object import *

class enemy(Object):
    dir = None
    def detect(self, other):
        if self.CtoDcheck(other):
            if other.faction == 1:
                return True
        return False













