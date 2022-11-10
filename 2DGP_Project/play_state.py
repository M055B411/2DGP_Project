import random

from pico2d import *
import game_framework
import player
import object


worldtick = 0
Tile = None

def enter():
    global player, cursor, Tile
    hide_cursor()
    player = player.Player()
    cursor = object.cursor()
    Tile = load_image("temp_tile.png")
    pass

def exit():
    global player, cursor
    del player, cursor
    pass

def update():
    global worldtick
    worldtick = (worldtick + 1) % 60

    if worldtick == 0 and len(object.bomb.bomb_list) < 6:
        temp = object.bomb(random.randrange(50,750), random.randrange(50,550), 30)
        object.bomb.bomb_list.append(temp)
    player.update()
    for b in object.Bullet.Bullet_list:
        b.update()
    for b in object.bomb.bomb_list:
        b.update()
    pass

def draw():
    clear_canvas()
    Tile.draw(400, 300)
    player.draw()

    for b in object.bomb.bomb_list:
        if b.inexplo == True:
            b.explo_draw()
        else:
            b.draw()
    for b in object.Bullet.Bullet_list:
        b.draw()

    cursor.draw()
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            cursor.x = event.x
            cursor.y = 600 - event.y

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_w:
                player.move(0)
            elif event.key == SDLK_a:
                player.move(1)
            elif event.key == SDLK_s:
                player.move(2)
            elif event.key == SDLK_d:
                player.move(3)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                player.unmove(0)
            elif event.key == SDLK_a:
                player.unmove(1)
            elif event.key == SDLK_s:
                player.unmove(2)
            elif event.key == SDLK_d:
                player.unmove(3)
            elif event.key == SDLK_p:
                for b in object.bomb.bomb_list:
                    if b.inexplo == False:
                        b.explosion()
        elif player.state != player.statement['move'] and event.type == SDL_MOUSEMOTION:
            player.mouse_action(event.x, event.y)

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            player.state = player.statement['shoot']
            temp = object.Bullet(player.x, player.y, event.x, event.y)
            temp.addlist()

    pass

def pause(): pass

def resume(): pass
