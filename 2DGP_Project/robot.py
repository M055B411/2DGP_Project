import play_state
from Enemy import *
from bullet import Bullet


class Robot(enemy):
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
        if Robot.image == None:
            Robot.image = load_image('resource/enemy.png')

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
                game_world.remove_collision_object(self)

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
        game_world.add_collision_pairs(None, temp, 'ally:E-Bullet')

    def handle_collision(self, other, group):
        pass
