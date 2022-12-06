from pico2d import *

class Cursor:
    def __init__(self):
        self.image = load_image("resource/cursor.png")
        self.x, self.y = 400, 300

    def draw(self):
        self.image.clip_draw(50, 1, 48, 48, self.x, self.y)

    def update(self):
        pass

    def exit(self):
        pass
