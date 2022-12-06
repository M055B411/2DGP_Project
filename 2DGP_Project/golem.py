from Enemy import *
from car import CARBullet


class Golem(enemy):
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
        if Golem.image == None:
            Golem.image = load_image('resource/enemy.png')

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
                    game_world.remove_collision_object(self)

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
        game_world.add_collision_pairs(None, temp, 'ally:E-Bullet')
        self.Range = 300

    def handle_collision(self, other, group):
        if 'ally:enemy' == group:
            if self.state == 'ATTACK':
                other.hp -= self.damage
        pass