from object import *

class Block(Object):
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 0
        self.size = 32
        self.frame = random.randrange(0, 2)

        if Block.image == None:
            Block.image = load_image('resource/block.png')

    def update(self):
        pass

    def draw(self):
        if self.frame == 0:
            self.image.clip_draw(1, 79-33, 32, 32, self.x, self.y)
        elif self.frame == 1:
            self.image.clip_draw(40, 79-33, 32, 32, self.x, self.y)
        pass

    def exit(self):
        pass

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
        pass