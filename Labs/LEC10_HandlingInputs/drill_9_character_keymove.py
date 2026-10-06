import math

from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH, FRAME_HEIGHT = 100, 100
FRAME_COUNT = 8
MOVE_SPEED = 10
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


def update_position():
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
        x += horizontal / magnitude * MOVE_SPEED
        y += vertical / magnitude * MOVE_SPEED

    x = max(FRAME_WIDTH // 2, min(x, TUK_WIDTH - FRAME_WIDTH // 2))
    y = max(FRAME_HEIGHT // 2, min(y, TUK_HEIGHT - FRAME_HEIGHT // 2))


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
facing = 'right'
frame = 0
is_moving = False
pressed_keys = set()

while running:
    handle_events()
    if not running:
        break
    update_position()
    if is_moving:
        frame = (frame + 1) % FRAME_COUNT
        animation_row = RUN_ROW_BY_FACING[facing]
    else:
        frame = 0
        animation_row = IDLE_ROW_BY_FACING[facing]
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character_sheet.clip_draw(frame * FRAME_WIDTH, animation_row * FRAME_HEIGHT,
                              FRAME_WIDTH, FRAME_HEIGHT,
                              x, y)
    update_canvas()
    delay(0.05)

close_canvas()