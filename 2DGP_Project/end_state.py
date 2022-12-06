import game_framework
from pico2d import *
running = True
image = None
logo_time = 0.0
def enter():
    global image
    image = load_image('resource/game_over.png')
    pass
def exit():
    global image
    del image
    pass

import title_state
def update():
    pass
def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                game_framework.change_state(title_state)