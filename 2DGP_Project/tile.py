from pico2d import *

class Tile:
    def __init__(self):
        self.image = load_image("temp_tile.png")
        self.x, self.y = 400, 300

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

    def exit(self):
        pass
