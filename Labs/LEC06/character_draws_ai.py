from pico2d import *
import math
from pathlib import Path


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CENTER_X = CANVAS_WIDTH / 2
CENTER_Y = CANVAS_HEIGHT / 2
PATH_MARGIN = 50
FRAME_DELAY = 0.01


def draw_character(x, y):
	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(FRAME_DELAY)


def move_circle():
	radius = 200
	for degree in range(360):
		angle = math.radians(degree)
		x = CENTER_X + radius * math.cos(angle)
		y = CENTER_Y + radius * math.sin(angle)
		draw_character(x, y)


def move_line(start_x, start_y, end_x, end_y):
	distance = max(abs(end_x - start_x), abs(end_y - start_y))
	steps = int(distance)
	for step in range(steps + 1):
		progress = step / steps
		x = start_x + (end_x - start_x) * progress
		y = start_y + (end_y - start_y) * progress
		draw_character(x, y)


def move_rectangle():
	left = PATH_MARGIN
	right = CANVAS_WIDTH - PATH_MARGIN
	bottom = PATH_MARGIN
	top = CANVAS_HEIGHT - PATH_MARGIN

	move_line(left, top, right, top)
	move_line(right, top, right, bottom)
	move_line(right, bottom, left, bottom)
	move_line(left, bottom, left, top)


def move_triangle():
	left = PATH_MARGIN
	right = CANVAS_WIDTH - PATH_MARGIN
	bottom = PATH_MARGIN
	top = CANVAS_HEIGHT - PATH_MARGIN
	peak_x = CANVAS_WIDTH / 2

	move_line(left, bottom, peak_x, top)
	move_line(peak_x, top, right, bottom)
	move_line(right, bottom, left, bottom)


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
character = load_image(str(Path(__file__).with_name('character.png')))

try:
	while True:
		move_circle()
		move_rectangle()
		move_triangle()
finally:
	close_canvas()
