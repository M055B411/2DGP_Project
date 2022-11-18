import object
from object import *

class enemy(Object):
    dir = None
    def detect(self, other):
        if self.CtoDcheck(other):
            if other.faction == 1:
                return True
        return False



class enemy1(enemy):
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 5
        self.size = 26
        self.tick = 0
        self.damage = 2
        self.faction = 2
        self.frame = 0
        self.dir = -1
        self.Range = 200
        self.state = 'IDLE'
        self.target = None
        if enemy1.image == None:
            enemy1.image = load_image('enemy.png')

    def draw(self):
        if self.state == 'IDLE':
            if self.dir == 1:
                self.image.clip_draw(5 + 30 * self.frame, 727 - 26, 26, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 30 * self.frame, 727 - 26, 26, 26, 0, 'h', self.x, self.y, 30, 26)
        if self.state == 'MOVE':
            if self.dir == 1:
                self.image.clip_draw(5 + 30 * self.frame, 727 - 26*2, 26, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 30 * self.frame, 727 - 26*2, 26, 26, 0, 'h', self.x, self.y, 30, 26)
        if self.state == 'DEAD':
            if self.dir == 1:
                self.image.clip_draw(5 + 30 * (self.frame+3), 727 - 26*3, 32, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5+ 30 * (self.frame+3), 727 - 26*3, 32, 26, 0, 'h', self.x, self.y, 30, 26)
            if self.frame == 4:
                game_world.remove_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.state != 'DEAD':
            if self.target == None:
                for o in game_world.objects[2]:
                    if self.detect(o):
                        self.target = o
            else:
                if self.target.hp <= 0:
                    self.target = None
                elif self.x > self.target.x:
                    self.dir = -1
                elif self.x < self.target.x:
                    self.dir = 1
                if self.target != None and self.CtoDcheck(self.target):
                    self.state = 'IDLE'
                    if self.tick % 20 == 0:
                        self.attack(self.target)
                else:
                    self.moveto(self.target)
        if self.tick % 10 == 0:
            self.frame = (self.frame + 1) % 6
        if self.hp <= 0 and self.state != 'DEAD':
            self.state = 'DEAD'
            self.frame = 0
        pass


    def move(self):
        self.state = 'MOVE'
        pass

    def moveto(self, other):
        if other != None:
            self.state = 'MOVE'
            self.angle = math.atan2(other.y - self.y, other.x - self.x)
            self.x += 2 * math.cos(self.angle)
            self.y += 2 * math.sin(self.angle)

    def attack(self, other):
        temp = Bullet(self.x, self.y, other.x, other.y, faction = 2)
        game_world.add_object(temp, 3)


class enemy2(enemy):
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 5
        self.size = 26
        self.tick = 0
        self.damage = 1
        self.faction = 2
        self.frame = 0
        self.dir = -1
        self.Range = 100
        self.state = 'IDLE'
        self.cnt = 0
        self.target = None
        if enemy2.image == None:
            enemy2.image = load_image('enemy.png')

    def draw(self):
        if self.state == 'IDLE':
            if self.dir == 1:
                self.image.clip_draw(5 + 39 * self.frame, 727 - 106, 40, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 39 * self.frame, 727 - 106, 40, 26, 0, 'h', self.x, self.y, 40, 26)
        if self.state == 'MOVE':
            if self.dir == 1:
                self.image.clip_draw(5 + 42 * self.frame, 727 - (80 + 27 * 2), 40, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 42 * self.frame, 727 - (80 + 27 * 2), 40, 26, 0, 'h', self.x, self.y, 40, 26)
        if self.state == 'ATTACK':
            if self.dir == 1:
                self.image.clip_draw(5 + 39 * (self.frame+1), 727 - (80 + 27*3), 40, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 39 * (self.frame+1), 727 - (80 + 27*3), 40, 26, 0, 'h', self.x, self.y, 40, 26)
        if self.state == 'DEAD':
            if self.dir == 1:
                self.image.clip_draw(5 + 40 * (self.frame+2), 727 - (80 + 27 * 4), 40, 26, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 40 * (self.frame+2), 727 - (80 + 27 * 4), 40, 26, 0, 'h', self.x, self.y, 40, 26)
            if self.frame == 4:
                game_world.remove_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.state != 'DEAD' and self.state != 'ATTACK':
            if self.target == None:
                for o in game_world.objects[2]:
                    if self.detect(o):
                        self.target = o
            else:
                if self.target.hp <= 0:
                    self.target = None
                elif self.x > self.target.x:
                    self.dir = -1
                elif self.x < self.target.x:
                    self.dir = 1
                if self.target != None and self.CtoDcheck(self.target):
                    if self.state != 'ATTACK':
                        self.attack(self.target)
                else:
                    self.moveto(self.target)
                    if self.tick == 0:
                        self.cnt += 1
                    if self.cnt == 2:
                        self.cnt = 0
                        self.target = None
                        self.state = 'IDLE'
        elif self.state == 'ATTACK':
            if self.x > self.target.x:
                self.dir = -1
            elif self.x < self.target.x:
                self.dir = 1
            self.moveto(self.target)
            for o in game_world.objects[2]:
                if self.StoScheck(o):
                    if self.faction != o.faction:
                        o.hp -= self.damage
            if self.tick == 0:
                self.cnt += 1
            if self.cnt == 2:
                self.cnt = 0
                self.state = 'IDLE'
        if self.tick % 10 == 0:
            if self.state == 'IDLE':
                self.frame = (self.frame + 1) % 11
            elif self.state == 'MOVE':
                self.frame = (self.frame + 1) % 6
            elif self.state == 'ATTACK':
                self.frame = (self.frame + 1) % 5
            elif self.state == 'DEAD':
                self.frame = (self.frame + 1)
        if self.hp <= 0 and self.state != 'DEAD':
            self.state = 'DEAD'
            self.frame = 0
        pass



    def moveto(self, other):
        if other != None:
            self.angle = math.atan2(other.y - self.y, other.x - self.x)
            if self.state == 'ATTACK':
                self.x += 3 * math.cos(self.angle)
                self.y += 3 * math.sin(self.angle)
            else:
                self.state = 'MOVE'
                self.x += 1 * math.cos(self.angle)
                self.y += 1 * math.sin(self.angle)

    def attack(self, other):
        self.cnt = 0
        self.state = 'ATTACK'


class enemy3(enemy):
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 15
        self.size = 34
        self.tick = 0
        self.damage = 4
        self.faction = 2
        self.frame = 0
        self.dir = -1
        self.Range = 150
        self.state = 'IDLE'
        self.cnt = 0
        self.target = None
        if enemy3.image == None:
            enemy3.image = load_image('enemy.png')

    def draw(self):
        if self.state == 'IDLE':
            if self.dir == 1:
                self.image.clip_draw(5 + 49 * self.frame, 727 - 547, 49, 34, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 49 * self.frame, 727 - 547, 49, 34, 0, 'h', self.x, self.y, 49, 34)
        if self.state == 'MOVE':
            if self.dir == 1:
                self.image.clip_draw(5 + 50 * self.frame, 727 - 547 - 34, 49, 34, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 50 * self.frame, 727 - 547 - 34, 49, 34, 0, 'h', self.x, self.y, 49, 34)
        if self.state == 'TELE':
            if self.dir == 1:
                self.image.clip_draw(5 + 49 * self.frame, 727 - 547 - 34 * 2, 49, 34, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 49 * self.frame, 727 - 547 - 34 * 2, 49, 34, 0, 'h', self.x, self.y, 49, 34)
        if self.state == 'DEAD':
            if self.dir == 1:
                self.image.clip_draw(5 + 49 * (self.frame+5), 727 - 547 - 34 * 2, 49, 34, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_composite_draw(5 + 49 * (self.frame+5), 727 - 547 - 34 * 2, 49, 34, 0, 'h', self.x, self.y, 49, 34)
            if self.frame == 4:
                game_world.remove_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.state != 'DEAD' and self.state != 'TELE':
            if self.target == None:
                for o in game_world.objects[2]:
                    if self.detect(o):
                        self.target = o
            else:
                if self.target.hp <= 0:
                    self.target = None
                elif self.x > self.target.x:
                    self.dir = -1
                elif self.x < self.target.x:
                    self.dir = 1
                if self.target != None and self.CtoDcheck(self.target):
                    self.state = 'IDLE'
                    if self.tick % 20 == 0:
                        self.attack(self.target)
                else:
                    self.moveto(self.target)
                    if self.tick == 0:
                        self.cnt += 1
                    if self.cnt == 2:
                        self.cnt = 0
                        self.teleport(self.target)
        elif self.state == "TELE":
            if self.frame == 2:
                self.x = self.target.x + random.randrange(- 70, 70)
                self.y = self.target.y + random.randrange(- 70, 70)
            if self.frame == 3:
                self.state = 'IDLE'
        if self.tick % 10 == 0:
            if self.state == 'IDLE':
                self.frame = (self.frame + 1) % 4
            elif self.state == 'MOVE':
                self.frame = (self.frame + 1) % 8
            elif self.state == 'TELE':
                self.frame = (self.frame + 1)
            elif self.state == 'DEAD':
                self.frame = (self.frame + 1)
        if self.hp <= 0 and self.state != 'DEAD':
            self.state = 'DEAD'
            self.frame = 0
        pass


    def teleport(self, other):
        if other != None:
            self.state = 'TELE'
            self.frame = 0

    def moveto(self, other):
        if other != None:
            self.angle = math.atan2(other.y - self.y, other.x - self.x)
            if self.state == 'ATTACK':
                self.x += 3 * math.cos(self.angle)
                self.y += 3 * math.sin(self.angle)
            else:
                self.state = 'MOVE'
                self.x += 1 * math.cos(self.angle)
                self.y += 1 * math.sin(self.angle)

    def attack(self, other):
        temp = Bullet(self.x, self.y, other.x, other.y, faction=2)
        game_world.add_object(temp, 3)


class enemy4(enemy):
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 30
        self.size = 40
        self.tick = 0
        self.damage = 6
        self.faction = 2
        self.frame = 0
        self.dir = -1
        self.Range = 300
        self.state = 'IDLE'
        self.dodge = 0
        self.cnt = 0
        self.target = None
        self.hold = False
        if enemy4.image == None:
            enemy4.image = load_image('enemy.png')

    def draw(self):
        if self.hold:
            if self.state == 'HOLD':
                if self.dir == 1:
                    self.image.clip_draw(5 + 39 * self.frame, 727 - 358, 42, 42, self.x, self.y, 60, 60)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 39 * self.frame, 727 - 358, 42, 42, 0, 'h', self.x, self.y, 60,
                                                   60)
                if self.frame == 4:
                    self.state = 'IDLE'
            if self.state == 'IDLE':
                if self.dir == 1:
                    self.image.clip_draw(5 + 42 * self.frame, 727 - (358+42*1), 42, 42, self.x, self.y, 60, 60)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 42 * self.frame, 727 - (358+42*1), 42, 42, 0, 'h', self.x, self.y, 60,
                                                   60)
            if self.state == 'MOVE':
                if self.dir == 1:
                    self.image.clip_draw(5 + 43 * self.frame, 727 - (358+42*2), 42, 42, self.x, self.y, 60, 60)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 43 * self.frame, 727 - (358+42*2), 42, 42, 0, 'h', self.x,
                                                   self.y, 60, 60)
            if self.state == 'ATTACK':
                if self.dir == 1:
                    self.image.clip_draw(5 + 44 * (4-self.frame), 727 - 358 + 42, 42, 42, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 44 * (4-self.frame), 727 - 358 + 42, 42, 42, 0, 'h', self.x,
                                                   self.y, 60, 40)
            if self.state == 'DEAD':
                if self.dir == 1:
                    self.image.clip_draw(95 + 43 * self.frame, 727 - 518, 40, 26, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(95 + 43 * self.frame, 727 - 518, 40, 26, 0, 'h', self.x, self.y, 60,
                                                   40)
                if self.frame == 4:
                    game_world.remove_object(self)
        else:
            if self.state == 'IDLE':
                if self.dir == 1:
                    self.image.clip_draw(5 + 39 * self.frame, 727 - 220, 40, 26, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 39 * self.frame, 727 - 220, 40, 26, 0, 'h', self.x, self.y, 60, 40)
            if self.state == 'MOVE':
                if self.dir == 1:
                    self.image.clip_draw(5 + 42 * self.frame, 727 - (220 + 30 * 1), 40, 26, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 42 * self.frame, 727 - (220 + 30 * 1), 40, 26, 0, 'h', self.x, self.y, 60, 40)
            if self.state == 'ATTACK':
                if self.dir == 1:
                    self.image.clip_draw(5 + 50 * self.frame, 727 - (220 + 30*2), 50, 26, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(5 + 50 * self.frame, 727 - (220 + 30*2), 40, 26, 0, 'h', self.x, self.y, 60, 40)
            if self.state == 'DEAD':
                if self.dir == 1:
                    self.image.clip_draw(95 + 43 * self.frame, 727 - 518, 40, 26, self.x, self.y, 60, 40)
                elif self.dir == -1:
                    self.image.clip_composite_draw(95 + 43 * self.frame, 727 - 518, 40, 26, 0, 'h', self.x, self.y, 60, 40)
                if self.frame == 4:
                    game_world.remove_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.state != 'DEAD' and self.state != 'ATTACK':
            if self.target == None:
                for o in game_world.objects[2]:
                    if self.detect(o):
                        self.target = o
            else:
                if self.target.hp <= 0:
                    self.target = None
                elif self.x > self.target.x:
                    self.dir = -1
                elif self.x < self.target.x:
                    self.dir = 1
                if self.target != None and self.CtoDcheck(self.target):
                    if self.state != 'ATTACK':
                        if self.StoScheck(self.target) and self.target.faction == self.faction:
                            game_world.remove_object(self.target)
                            self.target = None
                            self.hold = True
                            self.state = 'HOLD'
                            self.Range = 500
                        for o in game_world.objects[1]:
                            if self.CtoDcheck(o) and o.faction == self.faction and not self.hold:
                                self.target = o
                        if self.target != None and self.dodge <= 0 and self.target.faction == 1:
                            self.frame = 0
                            if self.hold:
                                self.throw()
                                self.hold = False
                                self.state = 'IDLE'
                                self.dodge = 10
                            else:
                                self.attack(self.target)
                        else:
                            self.moveto(self.target)
                            if self.tick % 30 == 0:
                                self.dodge -= 1
                else:
                    self.moveto(self.target)
                    if self.tick == 0:
                        self.cnt += 1
                    if self.cnt == 2:
                        self.cnt = 0
                        self.target = None
                        self.state = 'IDLE'
        elif self.state == 'ATTACK':
            if self.x > self.target.x:
                self.dir = -1
            elif self.x < self.target.x:
                self.dir = 1
            if not self.hold:
                self.moveto(self.target)
                for o in game_world.objects[2]:
                    if self.StoScheck(o):
                        if self.faction != o.faction:
                            o.hp -= self.damage
                if self.frame == 2:
                    self.frame = 0
                    self.dodge = 10
                    self.state = 'IDLE'
        if self.tick % 10 == 0:
            if self.hold:
                if self.state == 'IDLE':
                    self.frame = (self.frame + 1) % 6
                elif self.state == 'MOVE':
                    self.frame = (self.frame + 1) % 8
                elif self.state == 'ATTACK':
                    self.frame = (self.frame + 1) % 5
                elif self.state == 'DEAD':
                    self.frame = (self.frame + 1)
                elif self.state == 'HOLD':
                    self.frame = (self.frame + 1)
            else:
                if self.state == 'IDLE':
                    self.frame = (self.frame + 1) % 5
                elif self.state == 'MOVE':
                    self.frame = (self.frame + 1) % 6
                elif self.state == 'ATTACK':
                    self.frame = (self.frame + 1) % 3
                elif self.state == 'DEAD':
                    self.frame = (self.frame + 1)
                elif self.state == 'HOLD':
                    self.frame = (self.frame + 1)
        if self.hp <= 0 and self.state != 'DEAD':
            self.state = 'DEAD'
            self.frame = 0
        pass



    def moveto(self, other):
        if other != None:
            self.angle = math.atan2(other.y - self.y, other.x - self.x)
            if self.state == 'ATTACK':
                self.x += 5 * math.cos(self.angle)
                self.y += 5 * math.sin(self.angle)
            else:
                self.state = 'MOVE'
                if self.hold:
                    self.x += 0.5 * math.cos(self.angle)
                    self.y += 0.5 * math.sin(self.angle)
                else:
                    self.x += 1 * math.cos(self.angle)
                    self.y += 1 * math.sin(self.angle)

    def attack(self, other):
        self.cnt = 0
        self.state = 'ATTACK'

    def throw(self):
        self.cnt = 0
        self.state = 'ATTACK'
        temp = CARBullet(self.x, self.y, self.target.x, self.target.y)
        game_world.add_object(temp, 3)
        self.Range = 300




