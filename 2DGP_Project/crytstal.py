from object import *

class Crystal(Object):
    image =None

    def __init__(self):
        self.x = 400
        self.y = 360
        self.hp = 100
        self.faction = 1
        self.frame = 0
        self.tick = 0
        self.state = 'IDLE'

        if Crystal.image == None:
            Crystal.image = load_image('resource/crystal.png')

    def update(self):
        self.tick = (self.tick + 1) % 20
        if self.tick == 0:
            self.frame = (self.frame + 1) % 5

        if self.hp <= 0:
            self.state = 'DEATH'
        pass

    def draw(self):
        if self.state == 'IDLE':
            self.image.clip_draw(1 + 43 * self.frame, 485 - 100, 42, 89, self.x, self.y)
        elif self.state == 'DEATH':
            self.image.clip_draw(1 + 43 * self.frame, 485 - 413, 42, 89, self.x, self.y)
            if self.frame == 4:
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
        pass

    def exit(self):
        pass

    def get_bb(self):
        return self.x - 21, self.y - 45, self.x + 21, self.y + 45
        pass

    def handle_collision(self, other, group):
        pass