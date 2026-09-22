# 실습 과제 진행
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

def move_circle():
    print('circle')
    #캐릭터 이미지 표시
    clear_canvas()
    character.draw(400, 300)
    update_canvas()

def move_rectangle():
    print('rectangle')

def move_triangle():
    print('triangle')

while True:
    move_circle()
    move_rectangle()
    move_triangle()