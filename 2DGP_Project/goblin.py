import play_state
from Enemy import *
from bullet import Bullet


class Goblin(enemy):
    image = None
    attack_sound = None
    death_sound = None
    def __init__(self, x, y, faction = None):
        self.x = x
        self.y = y
        self.hp = 5
        self.size = 26
        self.tick = 0
        self.damage = 2
        if faction == None:
            self.faction = 2
        else:
            self.faction = faction
        self.frame = 0
        self.dir = -1
        self.Range = 200
        self.state = 'IDLE'
        self.target = None
        if Goblin.image == None:
            Goblin.image = load_image('resource/enemy.png')
        if Goblin.attack_sound == None:
            Goblin.attack_sound = load_wav('resource/sound/goblin_attack.wav')
        Goblin.attack_sound.set_volume(32)
        if Goblin.death_sound == None:
            Goblin.death_sound = load_wav('resource/sound/goblin_death.wav')
        Goblin.death_sound.set_volume(32)

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
                game_world.remove_collision_object(self)

        pass

    def update(self):
        self.tick = (self.tick + 1) % 60
        if self.tick % 10 == 0:
            self.frame = (self.frame + 1) % 6
        if self.state != 'DEAD':
            if self.target == None:
                self.find_target()
            else:
                if self.target.hp <= 0:
                    self.target = None
                elif self.x > self.target.x:
                    self.dir = -1
                elif self.x < self.target.x:
                    self.dir = 1
                if self.CtoDcheck(self.target):
                    self.attack()
                else:
                    self.moveto()
            if self.hp <= 0 and self.state != 'DEAD':
                self.death_sound.play()
                self.state = 'DEAD'
                self.frame = 0
        pass

    def find_target(self):
        if self.target == None:
            for o in game_world.objects[2]:
                if self.detect(o):
                    self.target = o


    def move(self):
        self.state = 'MOVE'
        pass

    def moveto(self):
        if self.target != None:
            self.state = 'MOVE'
            self.angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
            self.x += 2 * math.cos(self.angle)
            self.y += 2 * math.sin(self.angle)

    def attack(self):
        if self.target != None and self.CtoDcheck(self.target):
            self.state = 'IDLE'
            if self.tick % 20 == 0:
                self.attack_sound.play()
                temp = Bullet(self.x, self.y, self.target.x, self.target.y, faction = self.faction)
                game_world.add_object(temp, 3)
                game_world.add_collision_pairs(None, temp, 'ally:E-Bullet')
                game_world.add_collision_pairs(None, temp, 'prop:bullet')


    def handle_collision(self, other, group):
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

