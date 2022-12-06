from pico2d import *
import server

class HP:
    image1 = None
    image2 = None
    def __init__(self):
        self.x = 130
        self.y = 40

        self.max_hp = 40
        self.cur_hp = server.player.hp

        if HP.image1 == None:
            HP.image1 = load_image('resource/HP_green.png')

        if HP.image2 == None:
            HP.image2 = load_image('resource/HP_red.png')

    def update(self):
        self.cur_hp = server.player.hp

    def draw(self):
        self.image2.draw(self.x, self.y)
        self.image1.clip_draw(0, 0, int((200 * (self.cur_hp / self.max_hp))), 25, self.x+(100*((self.cur_hp / self.max_hp)-1)), self.y)

    def exit(self):
        pass

class Item:
    image1 =None
    image2 =None

    def __init__(self):
        self.x = 670
        self.y = 40

        if HP.image1 == None:
            HP.image1 = load_image('resource/HP_green.png')

        if HP.image2 == None:
            HP.image2 = load_image('resource/HP_red.png')

