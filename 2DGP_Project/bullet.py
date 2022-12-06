from object import *

class Bullet(Object):
    image = None
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
            Bullet.image = load_image('resource/Player.png')

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
                    game_world.remove_collision_object(self)
        self.move()
        if self.x > 800 or self.x < 0:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)
        elif self.y > 600 or self.y < 0:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)


    def move(self):
        self.x += 5 * math.cos(self.angle)
        self.y += 5 * math.sin(self.angle)
        pass

    def draw(self):
        self.image.clip_draw(233, 768 - 43, 5, 5, self.x, self.y)

    def handle_collision(self, other, group):
        if 'ally:E-Bullet' == group:
                other.hp -= self.hp
        elif 'A-Bullet:enemy' == group:
                other.hp -= self.hp
        pass
