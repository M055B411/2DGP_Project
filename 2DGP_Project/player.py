from bullet import Bullet
from object import *



class Player(Object):
    image =None



    attack_sound = None
    death_sound = None
    def __init__(self):
        self.x, self.y = 400, 300
        self.statement = {'idle': 4, 'move': 2, 'shoot': 4, 'death': 5}
        self.look = {'front': 0, 'right': 1, 'back': 2, 'back_right': 3, 'left': 4, 'back_left': 6, 'front_left': 7, 'front_right': 8}
        self.hp = 20
        self.frame = 0
        self.tick = 0
        self.size = 22
        self.lookat = self.look['front']
        self.state = self.statement['idle']
        self.faction = 1
        if Player.image == None:
            Player.image = load_image("resource/Player.png")
        self.range = 10
        self.dirx, self.diry = 0, 0
        self.iscollidex, self.iscollidey = False, False

        if Player.attack_sound == None:
            Player.attack_sound = load_wav('resource/sound/player_attack.wav')
        Player.attack_sound.set_volume(32)

        if Player.death_sound == None:
            Player.death_sound = load_wav('resource/sound/player_death.wav')
        Player.attack_sound.set_volume(32)

        self.item = 'PISTOL'



    def handle_collision(self, other, group):
        pass


    def update(self):
        if self.state != 'death':
            if self.hp <= 0:
                print("player dead")
                self.state = 'death'
                self.death_sound.play()
                game_world.remove_collision_object(self)
            else:
                self.tick = (self.tick + 1) % 8
                if self.tick == 0:
                    self.frame = (self.frame + 1) % self.state

                self.state_check()

                if self.dirx == 1 and self.diry == 1:
                    self.x += 2/1.414
                    self.y += 2/1.414
                elif self.dirx == 1 and self.diry == -1:
                    self.x += 2/1.414
                    self.y -= 2/1.414
                elif self.dirx == -1 and self.diry == 1:
                    self.x -= 2/1.414
                    self.y += 2/1.414
                elif self.dirx == -1 and self.diry == -1:
                    self.x -= 2/1.414
                    self.y -= 2/1.414
                elif self.dirx == 1 and self.diry == 0:
                    self.x += 2
                elif self.dirx == -1 and self.diry == 0:
                    self.x -= 2
                elif self.dirx == 0 and self.diry == 1:
                    self.y += 2
                elif self.dirx == 0 and self.diry == -1:
                    self.y -= 2

                if self.x > 800:
                    self.x = 800
                if self.x < 0:
                    self.x = 0
                if self.y > 600:
                    self.y = 0
                if self.y < 0:
                    self.y = 0

    def draw(self):
        size = 22
        if self.lookat == self.look['front'] or self.lookat == self.look['back']:
            size = 22
        elif self.lookat == self.look['right'] or self.lookat == self.look['back_right'] \
                or self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
            size = 21
        if self.state == self.statement['idle'] or self.state == self.statement['shoot']:
            if self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
                self.image.clip_composite_draw(21 + self.frame * size, 768 - (59 + (self.lookat-3) * 25), 22, 22, 0, 'h', self.x, self.y, 22, 22)
            else:
                self.image.clip_draw(21 + self.frame * size, 768 - (59 + self.lookat * 25), 22, 22, self.x, self.y)
        elif self.state == self.statement['move']:
                if self.lookat == self.look['front']:
                    self.image.clip_draw(21 + (((self.frame + 1) * 3)-1) * 21, 768 - (175 + 1 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back']:
                    self.image.clip_draw(21 + (((self.frame + 1) * 3)-1) * 22, 768 - (176 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['left']:
                    self.image.clip_composite_draw(21 + self.frame * 21, 768 - (175 + 1 * 26), 22, 22, 0, 'h', self.x, self.y, 22, 22)
                elif self.lookat == self.look['right']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (175 + 1 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back_right']:
                    self.image.clip_draw(22 + (self.frame + 3) * 22, 768 - (175 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['back_left']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (175 + 2 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['front_right']:
                    self.image.clip_draw(21 + self.frame * 21, 768 - (173 + 0 * 26), 22, 22, self.x, self.y)
                elif self.lookat == self.look['front_left']:
                    self.image.clip_draw(21 + (self.frame + 3) * 21, 768 - (175 + 0 * 26), 22, 22, self.x, self.y)

            # if self.lookat == self.look['left'] or self.lookat == self.look['back_left']:
            #     self.image.clip_composite_draw(21 + self.frame * size, 768 - (59 + (self.lookat-3) * 25), 22, 22, 0, 'h', self.x, self.y, 22, 22)
            # else:
            #     self.image.clip_draw(21 + self.frame * size, 768 - (59 + self.lookat * 25), 22, 22, self.x, self.y)

    def move(self, direction):
        if direction == 0:
            self.diry += 1
        elif direction == 1:
            self.dirx += -1
        elif direction == 2:
            self.diry += -1
        elif direction == 3:
            self.dirx += 1

    def unmove(self, direction):
        if direction == 0:
            self.diry = 0
        elif direction == 1:
            self.dirx = 0
        elif direction == 2:
            self.diry = 0
        elif direction == 3:
            self.dirx = 0

    def state_check(self):
        if self.diry == 0 and self.dirx == 0:
            self.state = self.statement['idle']
        elif self.diry == 0 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['right']
        elif self.diry == 0 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['left']
        elif self.diry == 1 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['back_right']
        elif self.diry == 1 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['back_left']
        elif self.diry == 1 and self.dirx == 0:
            self.state = self.statement['move']
            self.lookat = self.look['back']
        elif self.diry == -1 and self.dirx == 1:
            self.state = self.statement['move']
            self.lookat = self.look['front_right']
        elif self.diry == -1 and self.dirx == -1:
            self.state = self.statement['move']
            self.lookat = self.look['front_left']
        elif self.diry == -1 and self.dirx == 0:
            self.state = self.statement['move']
            self.lookat = self.look['front']

        pass

    def mouse_action(self, x, y):
        if self.x == x:
            if self.y > y:
                self.lookat = self.look['back']
            elif self.y <= y:
                self.lookat = self.look['front']
        elif self.y < y:
            if self.x < x:
                self.lookat = self.look['right']
            elif self.x > x:
                self.lookat = self.look['left']
        elif self.y > y:
            if self.x < x:
                self.lookat = self.look['back_right']
            elif self.x > x:
                self.lookat = self.look['back_left']

    def shot_bullet(self, event):
        if self.item == 'PISTOL':
            self.attack_sound.play()
            self.state = self.statement['shoot']
            temp = Bullet(self.x, self.y, event.x, 600 - event.y, faction=self.faction)
            game_world.add_object(temp, 3)
            game_world.add_collision_pairs(temp, None, 'A-Bullet:enemy')
            game_world.add_collision_pairs(None, temp, 'prop:bullet')
        if self.item == 'SHOTGUN':
            self.attack_sound.play()
            self.state = self.statement['shoot']
            for i in range(0, 4):
                temp = Bullet(self.x, self.y, (event.x + random.randrange(0, 40)), 600 - (event.y + random.randrange(0,40)), faction=self.faction)
                game_world.add_object(temp, 3)
                game_world.add_collision_pairs(temp, None, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:bullet')

    def handle_collision(self, other, group):
        if 'prop:player' == group:
            if other.x > self.x:
                self.x -= other.size / 2
            elif other.x < self.x:
                self.x += other.size / 2

            if other.y > self.y:
                self.y -= other.size / 2
            elif other.y < self.y:
                self.y += other.size / 2

        pass