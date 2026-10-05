import math
from pathlib import Path

from pico2d import (
	SDL_KEYDOWN,
	SDL_QUIT,
	SDLK_ESCAPE,
	clear_canvas,
	close_canvas,
	delay,
	get_events,
	get_time,
	load_font,
	load_image,
	open_canvas,
	update_canvas,
)

CANVAS_W, CANVAS_H = 800, 600
SCALE = 3
FPS_DELAY = 0.08
REPEAT_COUNT = 5
PAUSE_SEC = 1.0
SHEET_W, SHEET_H = 399, 525

# Each frame is (left, top, width, height), measured from the supplied sheet.
ANIMATIONS = (
	("Run", 0.08, (
		(1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
		(86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
		(182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
		(270, 45, 24, 32), (302, 51, 29, 26),
	)),

