from object import *



class Player(Object):
    def __init__(self):
        self.x, self.y = 400, 300
        self.statement = {'idle': 4, 'move': 2, 'shoot': 4}
        self.look = {'front': 0, 'right': 1, 'back': 2, 'back_right': 3, 'left': 4, 'back_left': 6, 'front_left': 7, 'front_right': 8}
        self.hp = 20
        self.frame = 0
        self.tick = 0
        self.size = 22
        self.lookat = self.look['front']
        self.state = self.statement['idle']
        self.faction = 1
        if Player.image == None:
            Player.image = load_image("Player.png")
        self.range = 10
        self.dirx, self.diry = 0, 0
        self.iscollidex, self.iscollidey = False, False

    def collision(self, other):
        if self.StoScheck(other):
            if self.faction != other.faction:
                print("collide")
                if self.x - self.size / 2 > other.x + other.size / 2:
                    self.x = other.x + other.size / 2 + self.size / 2
                elif self.x + self.size / 2 < other.x - other.size / 2:
                    self.x = other.x - other.size / 2 - self.size / 2
                elif self.y - self.size / 2 > other.y + other.size / 2:
                    self.y = other.y + other.size / 2 + self.size / 2
                elif self.y + self.size / 2 < other.y - other.size / 2:
                    self.y = other.y - other.size / 2 - self.size / 2


    def update(self):
        if self.hp == 0:
            print("player dead")
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

            for o in game_world.objects[1]:
                self.collision(o)
            for o in game_world.objects[2]:
                self.collision(o)

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