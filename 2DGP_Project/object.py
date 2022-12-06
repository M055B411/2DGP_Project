import random

from pico2d import *
import math
import game_world

class Object:

    def get_bb(self):
        return self.x - self.size/2, self.y - self.size/2, self.x + self.size/2, self.y + self.size/2
    # def StoScheck(self, other):
    #     if self.x - self.size / 2 > other.x + other.size / 2:
    #         return False
    #     elif self.x + self.size / 2 < other.x - other.size / 2:
    #         return False
    #     elif self.y - self.size / 2 > other.y + other.size / 2:
    #         return False
    #     elif self.y + self.size / 2 < other.y - other.size / 2:
    #         return False
    #     else:
    #         return True
    # pass


    def CtoDcheck(self, other):
        if other != None:
            a = self.x - other.x
            b = self.y - other.y
            if int(math.sqrt((a * a) + (b * b))) < self.Range:
                return True
        else:
            return False















