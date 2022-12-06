from pico2d import *

class Tile:
    def __init__(self):
        self.image = load_image("resource/background.png")
        self.music = load_music('resource/sound/tile.ogg')
        self.music.set_volume(32)
        self.music.repeat_play()
        self.x, self.y = 400, 300

    def draw(self):
        self.image.draw(self.x, self.y, 800, 600)

    def update(self):
        pass

    def exit(self):
        pass
