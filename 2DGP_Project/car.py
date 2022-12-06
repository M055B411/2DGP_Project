from object import *
from explosion import Explosion

class CARBullet(Object):
    image = None
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
            CARBullet.image = load_image('resource/enemy.png')
        self.Range = 80
        if hp == None:
            self.hp = 1
        else: self.hp = hp

    def update(self):
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


        if self.x > 800 or self.x < 0:
            game_world.remove_object(self)
        elif self.y > 600 or self.y < 0:
            game_world.remove_object(self)


    def move(self):
        self.x += 5 * math.cos(self.angle)
        self.y += 5 * math.sin(self.angle)
        pass

    def draw(self):
        self.image.clip_draw(92, 768 - 525, 35, 24, self.x, self.y, 40, 30)

    def explode(self):
        temp = Explosion(self.x, self.y, self.Range, Damage= self.damage)
        game_world.add_object(temp, 3)
        game_world.remove_object(self)
        game_world.remove_collision_object(self)

    def handle_collision(self, other, group):
        if 'ally:E-Bullet' == group:
            self.explode()
        pass
