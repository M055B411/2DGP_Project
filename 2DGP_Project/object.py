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

class Player(Object):
    def __init__(self):
        self.x, self.y = 400, 300
        self.statement = {'idle': 4, 'move': 2, 'shoot': 4}
        self.look = {'front': 0, 'right': 1, 'back': 2, 'back_right': 3, 'left': 4, 'back_left': 6, 'front_left': 7, 'front_right': 8}
        self.hp = 50
        self.frame = 0
        self.tick = 0
        self.lookat = self.look['front']
        self.state = self.statement['idle']
        self.image = load_image("Player.png")
        self.range = 10
        self.dirx, self.diry = 0, 0

    def update(self):
        self.tick = (self.tick + 1) % 8
        if self.tick == 0:
            self.frame = (self.frame + 1) % self.state

        self.state_check()
        if self.dirx == 1 and self.diry == 1:
            self.x += 2/1.414
            self.y += 2/1.414
        elif self.dirx == 1 and self.diry == -1:
            self.x += 2/1.414
            self.y -= 2/1.414
        elif self.dirx == -1 and self.diry == 1:
            self.x -= 2/1.414
            self.y += 2/1.414
        elif self.dirx == -1 and self.diry == -1:
            self.x -= 2/1.414
            self.y -= 2/1.414
        elif self.dirx == 1 and self.diry == 0:
            self.x += 2
        elif self.dirx == -1 and self.diry == 0:
            self.x -= 2
        elif self.dirx == 0 and self.diry == 1:
            self.y += 2
        elif self.dirx == 0 and self.diry == -1:
            self.y -= 2

    def draw(self):
        size = 22
        if self.lookat == self.look['front'] or self.lookat == self.look['back']:
            size = 22
        elif self.lookat == self.look['right'] or self.lookat == self.look['back_right'] \
                or self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
            size = 21
        if self.state == self.statement['idle'] or self.state == self.statement['shoot']:
            if self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
                self.image.clip_composite_draw(21 + self.frame * size, 768 - (59 + (self.lookat-3) * 25), 22, 22, 0, 'h', self.x, self.y, 22, 22)
            else:
                self.image.clip_draw(21 + self.frame * size, 768 - (59 + self.lookat * 25), 22, 22, self.x, self.y)
        elif self.state == self.statement['move']:
                if self.lookat == self.look['front']:
                    self.image.clip_draw(21 + (((self.frame + 1) * 3)-1) * 21, 768 - (175 + 1 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back']:
                    self.image.clip_draw(21 + (((self.frame + 1) * 3)-1) * 22, 768 - (176 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['left']:
                    self.image.clip_composite_draw(21 + self.frame * 21, 768 - (175 + 1 * 26), 22, 22, 0, 'h', self.x, self.y, 22, 22)
                elif self.lookat == self.look['right']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (175 + 1 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back_right']:
                    self.image.clip_draw(22 + (self.frame + 3) * 22, 768 - (175 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back_left']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (175 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['front_right']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (173 + 0 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['front_left']:
                    self.image.clip_draw(21 + (self.frame + 3) * 21, 768 - (175 + 0 * 26), 22, 22, self.x, self.y)

            # if self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
            #     self.image.clip_composite_draw(21 + self.frame * size, 768 - (59 + (self.lookat-3) * 25), 22, 22, 0, 'h', self.x, self.y, 22, 22)
            # else:
            #     self.image.clip_draw(21 + self.frame * size, 768 - (59 + self.lookat * 25), 22, 22, self.x, self.y)

    def move(self, direction):
        if direction == 0:
            self.diry = 1
        elif direction == 1:
            self.dirx = -1
        elif direction == 2:
            self.diry = -1
        elif direction == 3:
            self.dirx = 1

    def unmove(self, direction):
        if direction == 0:
            self.diry = 0
        elif direction == 1:
            self.dirx = 0
        elif direction == 2:
            self.diry = 0
        elif direction == 3:
            self.dirx = 0

    def state_check(self):
        if self.diry == 0 and self.dirx == 0:
            self.state = self.statement['idle']
        elif self.diry == 0 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['right']
        elif self.diry == 0 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['left']
        elif self.diry == 1 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['back_right']
        elif self.diry == 1 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['back_left']
        elif self.diry == 1 and self.dirx == 0:
            self.state = self.statement['move']
            self.lookat = self.look['back']
        elif self.diry == -1 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['front_right']
        elif self.diry == -1 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['front_left']
        elif self.diry == -1 and self.dirx == 0:
            self.state = self.statement['move']
            self.lookat = self.look['front']

        pass

    def mouse_action(self, x, y):
        if self.x == x:
            if self.y > y:
                self.lookat = self.look['back']
            elif self.y <= y:
                self.lookat = self.look['front']
        elif self.y < y:
            if self.x < x:
                self.lookat = self.look['right']
            elif self.x > x:
                self.lookat = self.look['left']
        elif self.y > y:
            if self.x < x:
                self.lookat = self.look['back_right']
            elif self.x > x:
                self.lookat = self.look['back_left']


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
        self.image = load_image('Player.png')
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