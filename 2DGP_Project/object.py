import random

from pico2d import *
import math
import game_world

class Object:

    def get_bb(self):
        return self.x - self.size/2, self.y - self.size/2, self.x + self.size/2, self.y + self.size/2
    def StoScheck(self, other):
        if self.x - self.size / 2 > other.x + other.size / 2:
            return False
        elif self.x + self.size / 2 < other.x - other.size / 2:
            return False
        elif self.y - self.size / 2 > other.y + other.size / 2:
            return False
        elif self.y + self.size / 2 < other.y - other.size / 2:
            return False
        else:
            return True
    pass


    def CtoDcheck(self, other):
        a = self.x - other.x
        b = self.y - other.y
        if int(math.sqrt((a * a) + (b * b))) < self.Range:
            return True
        else:
            return False











class CAR(Object):
    bomb_list = []
    image = None
    image2 = None

    def __init__(self , x, y, Range = None):
        self.x = x
        self.y = y
        self.hp = 20
        self.size = 40
        self.tick = 0
        self.inexplo = False
        self.damage = 2
        self.faction = 2
        if Range == None:
            Range == 80
        else: self.Range = Range
        if CAR.image == None:
            CAR.image = load_image('enemy.png')
        if CAR.image2 == None:
            CAR.image2 = load_image('Explosion.png')

    def draw(self):
        if self.inexplo:
            self.image2.clip_draw(64 * self.frame, 64, 64, 64, self.x, self.y, 80, 80)
        else:
            self.image.clip_draw(92, 768 - 525, 35, 24, self.x, self.y, 40, 30)

    def update(self):
        for o in game_world.objects[2]:
            if self.StoScheck(o):
                if self.x - self.size / 2 > o.x + o.size / 2:
                    o.x -= self.size/2 + o.size /2
                elif self.x + self.size / 2 < o.x - o.size / 2:
                    o.x += self.size/2 + o.size /2
                elif self.y - self.size / 2 > o.y + o.size / 2:
                    o.y -= self.size/2 + o.size /2
                elif self.y + self.size / 2 < o.y - o.size / 2:
                    o.y += self.size / 2 + o.size / 2
        if self.hp <= 0 and not self.inexplo:
            self.explosion()
        if self.inexplo:
            self.tick = (self.tick + 1) % 10
            if self.tick == 0:
                self.frame += 1
                for obj in game_world.layer_objects(2):
                    if self.CtoDcheck(obj):
                        obj.hp -= self.damage
            if self.frame == 4:
                game_world.remove_object(self)


    def explosion(self):
        self.inexplo = True
        self.frame = 0



