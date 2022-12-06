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
        for o in game_world.objects[2]:
            if self.StoScheck(o):
                if self.x - self.size / 2 > o.x + o.size / 2:
                    o.x -= self.size/2 + o.size /2
                elif self.x + self.size / 2 < o.x - o.size / 2:
                    o.x += self.size/2 + o.size /2
                elif self.y - self.size / 2 > o.y + o.size / 2:
                    o.y -= self.size/2 + o.size /2
                elif self.y + self.size / 2 < o.y - o.size / 2:
                    o.y += self.size / 2 + o.size / 2
        if self.hp <= 0:
            self.explosion()



    def explosion(self):
        temp = explosion.Explosion(self.x, self.y, Damage=self.damage, size=64, Range=64)
        game_world.add_object(temp, 3)
        game_world.remove_object(self)
        game_world.remove_collision_object(self)
        bomb.bomb_list.remove(self)

