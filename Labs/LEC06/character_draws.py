# 실습 과제 진행
from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)

def move_top():
    for x in range(50, 751, 5):
        clear_canvas()
        character.draw(x, 550)
        update_canvas()
        delay(0.01)
    pass

def move_right():
    pass

def move_bottom():
    pass

def move_left():
    pass

def move_rectangle():
    print('rectangle')
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_triangle():
    print('triangle')

while True:
    move_circle()
    move_rectangle()
    move_triangle()
