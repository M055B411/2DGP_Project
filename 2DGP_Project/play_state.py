from object import *
import game_framework
import game_world

from player import Player

worldtick = 0

def enter():
    global player, cursor, Tile
    hide_cursor()
    player = Player()
    cursor = cursor()
    Tile = Tile()

    game_world.add_object(Tile, 0)
    game_world.add_object(player, 2)
    game_world.add_object(cursor, 4)
    pass

def exit():
    global player, cursor, Tile
    del player, cursor, Tile
    pass

def update():
    global worldtick
    worldtick = (worldtick + 1) % 60

    if worldtick == 0 and len(bomb.bomb_list) < 6:
        temp = bomb(random.randrange(50,750), random.randrange(50,550), 30)
        bomb.bomb_list.append(temp)
        game_world.add_object(temp, 2)
    player.update()
    for game_object in game_world.all_objects():
        game_object.update()
    pass

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
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
                for b in bomb.bomb_list:
                    if b.inexplo == False:
                        b.explosion()
        elif player.state != player.statement['move'] and event.type == SDL_MOUSEMOTION:
            player.mouse_action(event.x, event.y)

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            player.state = player.statement['shoot']
            temp = Bullet(player.x, player.y, event.x, event.y, faction= 1)
            game_world.add_object(temp, 3)

    pass

def pause(): pass

def resume(): pass
