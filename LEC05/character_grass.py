from pico2d import *

open_canvas()
character = load_image('character.png')

while True:
    x = -200
    while x <= 200:
        clear_canvas()
        y = (200 ** 2 - x**2) ** 0.5
        character.draw(x + 400, y + 300)
        update_canvas()
        x += 2
        delay(0.01)
    x = 200
    while x >= -200:
        clear_canvas()
        y = (200 ** 2 - x**2) ** 0.5
        character.draw(x + 400, y + 300)
        update_canvas()
        x -= 2
        delay(0.01)       
close_canvas()