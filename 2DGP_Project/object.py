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
    faction = None
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
                bomb.bomb_list.remove(self)


    def explosion(self):
        self.inexplo = True
        self.frame = 0



class Bullet(Object):
    image2 = None
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
        self.angle = math.atan2(self.toy - self.y, self.tox - self.x)
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


class CARBullet(Object):
    image2 = None
    def __init__(self, x, y, x2, y2, hp = None):
        self.x = x
        self.y = y
        self.size = 24
        self.tox = x2
        self.toy = y2
        self.damage = 3
        self.frame = 0
        self.inexplo = False
        if self.x > self.tox:
            self.dir = -1
        elif self.x < self.tox:
            self.dir = 1
        self.faction = 2
        self.tick = 0
        self.angle = math.atan2(self.toy - self.y, self.tox - self.x)
        if CARBullet.image == None:
            CARBullet.image = load_image('enemy.png')
        if CARBullet.image2 == None:
            CARBullet.image2 = load_image('Explosion.png')
        self.Range = 80
        if hp == None:
            self.hp = 1
        else: self.hp = hp

    def update(self):
        if not self.inexplo:
            self.move()
            if self.dir == 1:
                if self.x > self.tox:
                    self.explode()
            elif self.dir == -1:
                if self.x < self.tox:
                    self.explode()
            for obj in game_world.layer_objects(1):
                if self.StoScheck(obj):
                    self.explode()
            for obj in game_world.layer_objects(2):
                if self.StoScheck(obj):
                    if self.faction != obj.faction:
                        print("collide")
                        self.explode()



        if self.inexplo:
            self.tick = (self.tick + 1) % 10
            if self.tick == 0:
                self.frame += 1
                for obj in game_world.layer_objects(2):
                    if self.CtoDcheck(obj):
                        obj.hp -= self.damage
            if self.frame >= 4:
                temp = CAR(self.x, self.y)
                game_world.add_object(temp, 1)
                game_world.remove_object(self)

        if self.x > 800 or self.x < 0:
            game_world.remove_object(self)
        elif self.y > 600 or self.y < 0:
            game_world.remove_object(self)


    def move(self):
        self.x += 5 * math.cos(self.angle)
        self.y += 5 * math.sin(self.angle)
        pass

    def draw(self):
        if self.inexplo:
            self.image2.clip_draw(64 * self.frame, 64, 64, 64, self.x, self.y, 80, 80)
        else:
            self.image.clip_draw(92, 768 - 525, 35, 24, self.x, self.y, 40, 30)

    def explode(self):
        self.inexplo = True
        self.frame = 0


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



