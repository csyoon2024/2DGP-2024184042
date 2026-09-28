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
        draw_character(x, y)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_top():
    for x in range(50, 751, 5):
        draw_character(x, 550)

def move_right():
    for y in range(550, 49, -5):
        draw_character(750, y)

def move_bottom():
    for x in range(750, 49, -5):
        draw_character(x, 50)

def move_left():
    for y in range(50, 551, 5):
        draw_character(50, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_line(x1, y1, x2, y2):
    for step in range(101):
        t = step / 100
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t

        draw_character(x, y)

def move_triangle():
    move_line(50, 50, 400, 550)
    move_line(400, 550, 750, 50)
    move_line(750, 50, 50, 50)

while True:
    move_circle()
    #move_rectangle()
    #move_triangle()
