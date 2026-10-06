import math
import time

from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH, FRAME_HEIGHT = 100, 100
FRAME_COUNT = 8
MOVE_SPEED = 200.0
FRAME_DURATION = 0.05
MAX_FRAME_DELTA = 0.1
IDLE_RIGHT_ROW, IDLE_LEFT_ROW = 3, 2
RUN_RIGHT_ROW, RUN_LEFT_ROW = 1, 0
IDLE_ROW_BY_FACING = {'right': IDLE_RIGHT_ROW, 'left': IDLE_LEFT_ROW}
RUN_ROW_BY_FACING = {'right': RUN_RIGHT_ROW, 'left': RUN_LEFT_ROW}
open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character_sheet = load_image('animation_sheet.png')


def handle_events():
    global running, pressed_keys

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in (SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT):
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update_position(delta_time):
    global x, y, facing, is_moving

    horizontal = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    vertical = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)

    if horizontal > 0:
        facing = 'right'
    elif horizontal < 0:
        facing = 'left'

    magnitude = math.hypot(horizontal, vertical)
    is_moving = magnitude > 0
    if magnitude:
        distance = MOVE_SPEED * delta_time
        x += horizontal / magnitude * distance
        y += vertical / magnitude * distance

    x = max(FRAME_WIDTH // 2, min(x, TUK_WIDTH - FRAME_WIDTH // 2))
    y = max(FRAME_HEIGHT // 2, min(y, TUK_HEIGHT - FRAME_HEIGHT // 2))


def update_animation(delta_time):
    global frame, animation_elapsed, animation_row

    if is_moving:
        animation_elapsed += delta_time
        while animation_elapsed >= FRAME_DURATION:
            frame = (frame + 1) % FRAME_COUNT
            animation_elapsed -= FRAME_DURATION
        animation_row = RUN_ROW_BY_FACING[facing]
    else:
        frame = 0
        animation_elapsed = 0
        animation_row = IDLE_ROW_BY_FACING[facing]


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
facing = 'right'
frame = 0
animation_elapsed = 0.0
is_moving = False
pressed_keys = set()
previous_time = time.perf_counter()

while running:
    current_time = time.perf_counter()
    delta_time = min(current_time - previous_time, MAX_FRAME_DELTA)
    previous_time = current_time
    handle_events()
    if not running:
        break
    update_position(delta_time)
    update_animation(delta_time)
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character_sheet.clip_draw(frame * FRAME_WIDTH, animation_row * FRAME_HEIGHT,
                              FRAME_WIDTH, FRAME_HEIGHT,
                              x, y)
    update_canvas()
    delay(0.01)

close_canvas()