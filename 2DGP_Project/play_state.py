import goblin
import wolf
from object import *
import game_framework
import game_world
from cursor import Cursor
from bullet import Bullet
from bomb import bomb
from goblin import Goblin
from wolf import Wolf
from robot import Robot
from golem import Golem

from player import Player

worldtick = 0

def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def enter():
    global player, cursor, Tile
    hide_cursor()
    player = Player()
    cursor = Cursor()
    # Tile = Tile()
    # game_world.add_object(Tile, 0)
    game_world.add_object(player, 2)
    game_world.add_object(cursor, 4)

    game_world.add_collision_pairs(player, None, 'ally:E-Bullet')
    game_world.add_collision_pairs(player, None, 'ally:enemy')
    game_world.add_collision_pairs(None, None, 'A-Bullet:enemy')
    pass

def exit():
    global player, cursor, Tile
    del player, cursor, Tile
    pass

def update():
    global worldtick
    worldtick = (worldtick + 1) % 60

    if worldtick == 0 and len(bomb.bomb_list) < 6:
        temp = bomb(random.randrange(50, 750), random.randrange(50, 550), 30)
        bomb.bomb_list.append(temp)
        game_world.add_object(temp, 2)
    player.update()
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
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
            elif event.key == SDLK_1:
                temp = Goblin(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
            elif event.key == SDLK_2:
                temp = Wolf(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
            elif event.key == SDLK_3:
                temp = Robot(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
            elif event.key == SDLK_4:
                temp = Golem(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                temp = CAR(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 1)
            elif event.key == SDLK_r:
                for o in game_world.objects[2]:
                    if o.faction == 2:
                        o.hp = 0
                for o in game_world.objects[1]:
                    game_world.remove_object(o)
                player.x = 400
                player.y = 300
                player.hp = 20
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
            temp = Bullet(player.x, player.y, event.x, 600 - event.y, faction= 1)
            game_world.add_object(temp, 3)
            game_world.add_collision_pairs(temp, None, 'A-Bullet:enemy')

    pass

def pause(): pass

def resume(): pass
