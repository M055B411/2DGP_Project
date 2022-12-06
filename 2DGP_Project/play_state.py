import wave
from car import CAR
from object import *
import game_framework
import game_world
from cursor import Cursor
from bomb import bomb
from goblin import Goblin
from wolf import Wolf
from robot import Robot
from golem import Golem
from crytstal import Crystal
from block import Block
from tile import Tile
import server
from ui import HP

from player import Player
import end_state

worldtick = 0
cooldown =0

round = 0
mobs =0

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
    global crystal, cursor, Tile, hp
    hide_cursor()
    server.player = Player()
    crystal = Crystal()
    hp = HP()
    cursor = Cursor()
    Tile = Tile()
    game_world.add_object(Tile, 0)
    game_world.add_object(crystal, 2)
    game_world.add_object(server.player, 2)
    game_world.add_object(hp, 4)
    game_world.add_object(cursor, 4)

    for i in range(0, 15):
        temp = Block(random.randrange(50, 750), random.randrange(50, 550))
        game_world.add_object(temp, 1)
        game_world.add_collision_pairs(temp, None, 'prop:enemy')
        game_world.add_collision_pairs(temp, None, 'prop:player')
        game_world.add_collision_pairs(temp, None, 'prop:bullet')
        game_world.add_collision_pairs(temp, temp, 'prop:prop')

    game_world.add_collision_pairs(server.player, None, 'ally:E-Bullet')
    game_world.add_collision_pairs(server.player, None, 'ally:enemy')
    game_world.add_collision_pairs(crystal, None, 'ally:E-Bullet')
    game_world.add_collision_pairs(crystal, None, 'ally:enemy')
    game_world.add_collision_pairs(None, None, 'A-Bullet:enemy')
    game_world.add_collision_pairs(None, None, 'prop:enemy')
    game_world.add_collision_pairs(None, server.player, 'prop:player')
    game_world.add_collision_pairs(None, None, 'prop:bullet')
    pass

def exit():
    global cursor, Tile
    del server.player, cursor, Tile
    pass

def update():
    global worldtick, cooldown, round, mobs
    if crystal.hp <= 0:
        game_framework.change_state(end_state)
    worldtick = (worldtick + 1) % 60
    if worldtick == 0:
        if server.player.hp <= 0:
            if server.cooldown == 0:
                server.player.hp = 40
                server.player.x = 400
                server.player.y = 300
                server.player.state = 'idle'

                game_world.add_object(server.player, 2)
                game_world.add_collision_pairs(server.player, None, 'ally:E-Bullet')
                game_world.add_collision_pairs(server.player, None, 'ally:enemy')
            else:
                print(server.cooldown)
                server.cooldown -= 1

        if cooldown == 0:
            if mobs == len(wave.wave_list[round]):
                if len(game_world.collision_group['prop:enemy'][1]) == 0:
                    cooldown = 20
                    mobs = 0
                    round += 1
            elif wave.wave_list[round][mobs] == 'goblin':
                temp = Goblin(random.randrange(50, 750), random.randrange(50, 550))
                temp.target = crystal
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
                mobs += 1
            elif wave.wave_list[round][mobs] == 'wolf':
                temp = Wolf(random.randrange(50, 750), random.randrange(50, 550))
                temp.target = crystal
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
                mobs += 1
            elif wave.wave_list[round][mobs] == 'robot':
                temp = Robot(random.randrange(50, 750), random.randrange(50, 550))
                temp.target = crystal
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
                mobs += 1
            elif wave.wave_list[round][mobs] == 'golems':
                temp = Golem(random.randrange(50, 750), random.randrange(50, 550))
                temp.target = crystal
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
                mobs += 1
        else:
            cooldown -= 1



    if worldtick == 0 and len(bomb.bomb_list) < 6:
        temp = bomb(random.randrange(50, 750), random.randrange(50, 550), 30)
        bomb.bomb_list.append(temp)
        game_world.add_object(temp, 2)
        game_world.add_collision_pairs(temp, None, 'prop:enemy')
        game_world.add_collision_pairs(temp, None, 'prop:player')
        game_world.add_collision_pairs(temp, None, 'prop:bullet')
        game_world.add_collision_pairs(temp, temp, 'prop:prop')
    if server.player.state != 'death':
        server.player.update()
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # print('COLLISION ', group)
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
                server.player.move(0)
            elif event.key == SDLK_a:
                server.player.move(1)
            elif event.key == SDLK_s:
                server.player.move(2)
            elif event.key == SDLK_d:
                server.player.move(3)
            elif event.key == SDLK_1:
                temp = Goblin(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
            elif event.key == SDLK_2:
                temp = Wolf(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
            elif event.key == SDLK_3:
                temp = Robot(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
            elif event.key == SDLK_4:
                temp = Golem(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 2)
                game_world.add_collision_pairs(None, temp, 'ally:enemy')
                game_world.add_collision_pairs(None, temp, 'A-Bullet:enemy')
                game_world.add_collision_pairs(None, temp, 'prop:enemy')
                game_world.add_collision_pairs(temp, temp, 'unit:unit')
                temp = CAR(random.randrange(50, 750), random.randrange(50, 550))
                game_world.add_object(temp, 1)
                game_world.add_collision_pairs(temp, None, 'prop:enemy')
                game_world.add_collision_pairs(temp, None, 'prop:player')
                game_world.add_collision_pairs(temp, None, 'prop:bullet')
                game_world.add_collision_pairs(temp, temp, 'prop:prop')
            elif event.key == SDLK_r:
                for o in game_world.objects[2]:
                    if o.faction == 2:
                        o.hp = 0
                for o in game_world.objects[1]:
                    game_world.remove_object(o)
                server.player.x = 400
                server.player.y = 300
                server.player.hp = 20
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                server.player.unmove(0)
            elif event.key == SDLK_a:
                server.player.unmove(1)
            elif event.key == SDLK_s:
                server.player.unmove(2)
            elif event.key == SDLK_d:
                server.player.unmove(3)
            elif event.key == SDLK_p:
                for b in bomb.bomb_list:
                     b.explosion()
        elif server.player.state != server.player.statement['move'] and event.type == SDL_MOUSEMOTION:
            server.player.mouse_action(event.x, event.y)

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if server.player.state != 'death':
                server.player.shot_bullet(event)

    pass

def pause(): pass

def resume(): pass
