from object import *
import explosion

class bomb(Object):
    bomb_list = []
    image = None

    def __init__(self , x, y, Range = None):
        self.x = x
        self.y = y
        self.hp = 5
        self.size = 21
        self.tick = 0
        self.damage = 2
        self.faction = 3
        if Range == None:
            Range == 64
        self.Range = Range
        self.frame = random.randrange(0, 7)
        if bomb.image == None:
            bomb.image = load_image('resource/bomb.png')

    def draw(self):
        self.image.clip_draw(5 + (21 * self.frame), 30, 21, 21, self.x, self.y)

    def update(self):
        if self.hp <= 0:
            self.explosion()



    def explosion(self):
        temp = explosion.Explosion(self.x, self.y, Damage=self.damage, size=64, Range=64)
        game_world.add_object(temp, 3)
        game_world.remove_object(self)
        game_world.remove_collision_object(self)
        bomb.bomb_list.remove(self)

    def handle_collision(self, other, group):
        if 'prob:player' == group or 'prop:enemy' == group:
            if other.x > self.x:
                other.x += self.size / 2
            elif other.x < self.x:
                other.x -= self.size / 2

            if other.y > self.y:
                other.y += self.size / 2
            elif other.y < self.y:
                other.y -= self.size / 2

        if 'prop:prop' == group:
            if other != self:
                if other.x > self.x:
                    self.x -= other.size / 2
                elif other.x < self.x:
                    self.x += other.size / 2

                if other.y > self.y:
                    self.y -= other.size / 2
                elif other.y < self.y:
                    self.y += other.size / 2

