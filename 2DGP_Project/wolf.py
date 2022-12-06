from Enemy import *


class Wolf(enemy):
    image = None

    attack_sound = None
    action_sound = None
    death_sound = None
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
        self.cooldown = 0
        self.target = None
        if Wolf.image == None:
            Wolf.image = load_image('resource/enemy.png')
        if Wolf.attack_sound == None:
            Wolf.attack_sound = load_wav('resource/sound/wolf_attack.wav')
        Wolf.attack_sound.set_volume(32)
        # if Wolf.action_sound == None:
        #     Wolf.action_sound = load_wav('resource/sound/wolf_action.wav')
        # Wolf.action_sound.set_volume(32)
        if Wolf.death_sound == None:
            Wolf.death_sound = load_wav('resource/sound/wolf_death.wav')
        Wolf.death_sound.set_volume(32)

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
                game_world.remove_collision_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.tick == 0 and self.cooldown != 0:
            self.cooldown -= 1
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
                    if self.state != 'ATTACK' and self.cooldown == 0:
                        self.attack(self.target)
                else:
                    self.moveto(self.target)
                    if self.tick == 0:
                        self.cnt += 1
                    if self.cnt == 6:
                        self.cnt = 0
                        self.target = None
                        self.state = 'IDLE'
                        self.cooldown = 5
        elif self.state == 'ATTACK':
            if self.x > self.target.x:
                self.dir = -1
            elif self.x < self.target.x:
                self.dir = 1
            self.moveto(self.target)
            if self.tick == 0:
                self.cnt += 1
            if self.cnt == 6:
                self.cnt = 0
                self.state = 'IDLE'
                self.cooldown = 5
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
            self.death_sound.play()
            self.state = 'DEAD'
            self.frame = 0
        pass



    def moveto(self, other):
        if other != None:
            self.angle = math.atan2(other.y - self.y, other.x - self.x)
            if self.state == 'ATTACK':
                self.x += 2.5 * math.cos(self.angle)
                self.y += 2.5 * math.sin(self.angle)
            else:
                self.state = 'MOVE'
                self.x += 1 * math.cos(self.angle)
                self.y += 1 * math.sin(self.angle)

    def attack(self, other):
        self.attack_sound.play()
        self.cnt = 0
        self.state = 'ATTACK'

    def handle_collision(self, other, group):
        if 'A-Bullet:enemy' == group:
            self.target = None
        if 'ally:enemy' == group:
            if self.state == 'ATTACK':
                other.hp -= self.damage
        if 'prop:enemy' == group:
            if self.state == 'ATTACK':
                other.hp -= self.damage
        if 'unit:unit' == group:
            if other != self:
                if other.x > self.x:
                    self.x -= other.size / 4
                elif other.x < self.x:
                    self.x += other.size / 4

                if other.y > self.y:
                    self.y -= other.size / 4
                elif other.y < self.y:
                    self.y += other.size / 4
        pass