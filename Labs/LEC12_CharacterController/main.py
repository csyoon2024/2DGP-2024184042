from pico2d import *
import random


# Game object class here
from boy import Boy
from grass import Grass





def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            boy.on_space()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            boy.on_direction_key_down(-1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            boy.on_direction_key_down(1)
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            boy.on_direction_key_up(-1)
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            boy.on_direction_key_up(1)


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
