from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH, FRAME_HEIGHT = 100, 100
FRAME_COUNT = 8
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


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
facing = 'right'
frame = 0
pressed_keys = set()

while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character_sheet.clip_draw(0, IDLE_ROW_BY_FACING['right'] * FRAME_HEIGHT,
                              FRAME_WIDTH, FRAME_HEIGHT,
                              x, y)
    update_canvas()
    handle_events()
    delay(0.05)

close_canvas()