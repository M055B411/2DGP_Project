import random

from pico2d import *
import math

class cursor:
    def __init__(self):
        self.image = load_image("cursor.png")
        self.x, self.y = 400, 300

    def draw(self):
        self.image.clip_draw(50, 1, 48, 48, self.x, self.y)

class Object:
    x = None
    y = None
    hp = None
    Range = None
    frame = None
    image = None

    def squareckeck(self, other):
        pass

    def roundcheck(self, other):
        pass




class bomb(Object):
    bomb_list = []
    def __init__(self , x, y, range = None):
        self.x = x
        self.y = y
        self.hp = 5
        self.tick = 0
        self.inexplo = False
        if range == None:
            range == 1
        self.range = range
        self.frame = random.randrange(0, 7)
        self.image = load_image('bomb.png')
        self.image2 = load_image('Explosion.png')

    def draw(self):
        self.image.clip_draw(5+(21*self.frame), 30, 21, 21, self.x, self.y)

    def explo_draw(self):
        self.image2.clip_draw(64 * self.frame, 64, 64, 64, self.x, self.y)

    def update(self):
        if self.hp == 0:
            self.explosion()
        if self.inexplo == True:
            self.tick = (self.tick + 1) % 10
            if self.tick == 0:
                self.frame += 1
            if self.frame == 4:
                self.bomb_list.remove(self)


    def explosion(self):
        self.inexplo = True
        self.frame = 0



class Bullet(Object):
    Bullet_list =[]

    def __init__(self, x, y, x2, y2, range = None, hp = None):
        self.x = x
        self.y = y
        self.tox = x2
        self.toy = y2
        self.angle = math.atan2(600 - self.toy - self.y, self.tox - self.x)
        if Bullet.image == None:
            Bullet.image = load_image('Player.png')
        if range == None:
            self.Range = 1
        else: self.Range = range
        if hp == None:
            self.hp = 1
        else: self.hp = hp

    def addlist(self):
        self.Bullet_list.append(self)

    def update(self):
        self.move()
        if self.x > 800 or self.x < 0:
            self.Bullet_list.remove(self)
        elif self.y > 600 or self.y < 0:
            self.Bullet_list.remove(self)

    def move(self):
        self.x += 5 * math.cos(self.angle)
        self.y += 5 * math.sin(self.angle)
        pass

    def draw(self):
        self.image.clip_draw(233, 768 - 43, 5, 5, self.x, self.y)