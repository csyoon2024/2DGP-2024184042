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
	("Run Fast", 0.06, (
		(8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
		(97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
		(206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
		(295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
	)),
	("Spin Dash", 0.07, (
		(1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
		(130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
	)),
	("Ball Roll", 0.08, (
		(1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
		(98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
		(193, 170, 30, 29), (230, 170, 31, 29), (268, 170, 30, 30),
	)),
	("Spin Attack", 0.07, (
		(1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
		(105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
	)),
	("Super Spin", 0.07, (
		(1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
		(111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
	)),
	("Spin Variant", 0.08, (
		(1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
		(123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
	)),
	("Idle", 0.12, (
		(1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
		(90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
		(184, 341, 40, 28), (232, 341, 39, 27),
	)),
	("Run Variant", 0.08, (
		(1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
		(99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
		(217, 379, 33, 36), (254, 378, 33, 36),
	)),
	("Hurt", 0.10, (
		(6, 429, 34, 40), (49, 426, 34, 43),
		(96, 427, 23, 39), (125, 427, 23, 39),
	)),
)


def get_source_rect(frame_rect):
	left, top, width, height = frame_rect
	if (
		left < 0
		or top < 0
		or width <= 0
		or height <= 0
		or left + width > SHEET_W
		or top + height > SHEET_H
	):
		raise ValueError(f"Frame is outside the sprite sheet: {frame_rect}")
	return left, SHEET_H - top - height, width, height


def draw_frame(image, frame_rect):
	source_x, source_y, frame_w, frame_h = get_source_rect(frame_rect)
	image.clip_draw(
		source_x,
		source_y,
		frame_w,
		frame_h,
		CANVAS_W // 2,
		CANVAS_H // 2,
		frame_w * SCALE,
		frame_h * SCALE,
	)


class AnimationSequence:
	def __init__(self, animations=ANIMATIONS):
		if not animations:
			raise ValueError("At least one animation is required")
		for name, frame_delay, frames in animations:
			if not name or frame_delay <= 0 or not frames:
				raise ValueError(f"Invalid animation: {name!r}")
			for frame_rect in frames:
				get_source_rect(frame_rect)
		self.animations = animations
		self.animation_index = 0
		self.frame_index = 0
		self.frame_timer = 0.0
		self.repeat_count = 0
		self.pause_started_at = None
		self.last_time = None

	@property
	def animation_name(self):
		return self.animations[self.animation_index][0]

	def update(self, current_time):
		if not math.isfinite(current_time):
			raise ValueError("Animation clock must return a finite time")
		elapsed = 0.0 if self.last_time is None else max(0.0, current_time - self.last_time)
		self.last_time = current_time

		if self.pause_started_at is not None:
			if current_time - self.pause_started_at >= PAUSE_SEC:
				self.animation_index = (self.animation_index + 1) % len(self.animations)
				self.frame_index = 0
				self.frame_timer = 0.0
				self.repeat_count = 0
				self.pause_started_at = None
		else:
			_, frame_delay, frames = self.animations[self.animation_index]
			self.frame_timer += elapsed
			while self.frame_timer + 1e-12 >= frame_delay:
				self.frame_timer = max(0.0, self.frame_timer - frame_delay)
				self.frame_index += 1
				if self.frame_index == len(frames):
					self.frame_index = 0
					self.repeat_count += 1
					if self.repeat_count == REPEAT_COUNT:
						self.pause_started_at = current_time
						self.frame_timer = 0.0
						break

		return self.animation_name, self.animations[self.animation_index][2][self.frame_index]



