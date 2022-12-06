import game_framework
from pico2d import *
running = True
image = None
logo_time = 0.0
def enter():
    global image
    image = load_image('resource/title.png')
    pass
def exit():
    global image
    del image
    pass

import play_state
def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
# game_framework.quit()
    delay(0.01)
    logo_time += 0.01
def draw():
    clear_canvas()
    image.draw(400, 300,800,600)
    update_canvas()
def handle_events():
    events = get_events()
    for event in events:
        if event.type ==SDL_QUIT:
            game_framework.quit()
        else:
            game_framework.change_state(play_state)