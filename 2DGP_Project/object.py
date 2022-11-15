import random

from pico2d import *
import math
import game_world

class cursor:
    def __init__(self):
        self.image = load_image("cursor.png")
        self.x, self.y = 400, 300

    def draw(self):
        self.image.clip_draw(50, 1, 48, 48, self.x, self.y)

    def update(self):
        pass

    def exit(self):
        pass

class Tile:
    def __init__(self):
        self.image = load_image("temp_tile.png")
        self.x, self.y = 400, 300

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

    def exit(self):
        pass


class Object:
    x = None
    y = None
    hp = 0
    size = 0
    Range = 0
    frame = 0
    image = None

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




class bomb(Object):
    bomb_list = []
    image = None
    image2 = None

    def __init__(self , x, y, Range = None):
        self.x = x
        self.y = y
        self.hp = 5
        self.size = 21
        self.tick = 0
        self.inexplo = False
        self.damage = 2
        self.faction = 3
        if Range == None:
            Range == 64
        self.Range = Range
        self.frame = random.randrange(0, 7)
        if bomb.image == None:
            bomb.image = load_image('bomb.png')
        if bomb.image2 == None:
            bomb.image2 = load_image('Explosion.png')

    def draw(self):
        if self.inexplo:
            self.image2.clip_draw(64 * self.frame, 64, 64, 64, self.x, self.y)
        else:
            self.image.clip_draw(5 + (21 * self.frame), 30, 21, 21, self.x, self.y)

    def update(self):
        if self.hp == 0:
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
                bomb.bomb_list.remove(self)


    def explosion(self):
        self.inexplo = True
        self.frame = 0



class Bullet(Object):

    def __init__(self, x, y, x2, y2, range = None, hp = None, faction = None):
        self.x = x
        self.y = y
        self.size = 5
        self.tox = x2
        self.toy = y2
        if faction == None:
            self.faction == None
        else:
            self.faction = faction
        self.angle = math.atan2(600 - self.toy - self.y, self.tox - self.x)
        if Bullet.image == None:
            Bullet.image = load_image('Player.png')
        if range == None:
            self.Range = 0
        else: self.Range = range
        if hp == None:
            self.hp = 1
        else: self.hp = hp

    def update(self):

        for obj in game_world.layer_objects(1):
            if self.StoScheck(obj):
                game_world.remove_object(self)
        for obj in game_world.layer_objects(2):
            if self.StoScheck(obj):
                if self.faction != obj.faction:
                    print("collide")
                    if self.Range == 0:
                        obj.hp -= self.hp
                    else:
                        for o in game_world.layer_objects(2):
                            if self.CtoDcheck(o):
                                o.hp -= self.hp
                    game_world.remove_object(self)
        self.move()
        if self.x > 800 or self.x < 0:
            game_world.remove_object(self)
        elif self.y > 600 or self.y < 0:
            game_world.remove_object(self)



    def move(self):
        self.x += 5 * math.cos(self.angle)
        self.y += 5 * math.sin(self.angle)
        pass

    def draw(self):
        self.image.clip_draw(233, 768 - 43, 5, 5, self.x, self.y)