from object import *

class Explosion(Object):
    image = None
    sound = None

    def __init__(self, x, y, Range=None, size = None, Damage = None):
        self.x = x
        self.y = y

        self.tick = 0
        if Damage == None:
            self.damage = 2
        else:
            self.damage = Damage
        if Range == None:
            self.Range == 64
        else:
            self.Range = Range
        if size == None:
            self.size = self.Range
        else:
            self.size = size

        self.frame = 0
        if Explosion.image == None:
            Explosion.image = load_image('resource/Explosion.png')
        self.sound_done = False
        if Explosion.sound == None:
            Explosion.sound = load_wav('resource/sound/explosion.wav')
        Explosion.sound.set_volume(32)

    def draw(self):
        self.image.clip_draw(64 * self.frame, 64, 64, 64, self.x, self.y, self.size, self.size)


    def update(self):
        self.tick = (self.tick + 1) % 10
        if self.frame == 0 and self.sound_done == False:
            self.sound.play()
            self.sound_done = True
        if self.tick == 0:
            self.frame += 1
            for obj in game_world.layer_objects(2):
                if self.CtoDcheck(obj):
                    obj.hp -= self.damage
        if self.frame == 4:
            game_world.remove_object(self)
            game_world.remove_collision_object(self)


    def handle_collision(self, other, group):
        pass
