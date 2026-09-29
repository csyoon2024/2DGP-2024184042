import math
from pathlib import Path

from pico2d import SDL_QUIT, close_canvas, clear_canvas, delay, get_events, get_time, load_image, open_canvas, update_canvas

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2
MIN_DISPLAY_HEIGHT = SCREEN_HEIGHT // 2
SPRITE_SHEET_WIDTH = 1792
SPRITE_SHEET_HEIGHT = 2358
FRAME_DURATION = 0.1
REPEAT_LIMIT = 5
PAUSE_DURATION = 1.0

ANIMATION_FRAMES = {
	"A": (
		(62, 141, 182, 243),
		(272, 142, 190, 242),
		(482, 141, 183, 243),
		(700, 142, 161, 242),
		(911, 142, 182, 242),
		(1121, 141, 183, 244),
		(1339, 142, 183, 243),
		(1550, 142, 168, 243),
	),
	"B": (
		(54, 570, 348, 364),
		(490, 563, 348, 378),
		(948, 563, 348, 363),
		(1378, 570, 340, 364),
	),
	"C": (
		(61, 1261, 198, 267),
		(302, 1193, 212, 335),
		(550, 1103, 205, 373),
		(828, 1209, 235, 319),
		(1121, 1239, 304, 290),
		(1454, 1224, 309, 312),
	),
	"D": (
		(68, 1865, 235, 336),
		(421, 1927, 200, 206),
		(767, 1903, 229, 230),
		(1105, 1843, 321, 321),
		(1513, 1911, 221, 222),
	),
}
ANIMATION_ORDER = ("A", "B", "C", "D")


def get_frame_source_rect(frame_rect):
	source_x, source_top, source_width, source_height = frame_rect
	source_y = SPRITE_SHEET_HEIGHT - source_top - source_height
	if (
		source_x < 0
		or source_top < 0
		or source_width <= 0
		or source_height <= 0
		or source_x + source_width > SPRITE_SHEET_WIDTH
		or source_top + source_height > SPRITE_SHEET_HEIGHT
	):
		raise ValueError(f"Frame rectangle is outside the sprite sheet: {frame_rect}")
	return source_x, source_y, source_width, source_height


def get_frame_destination_rect(frame_rect):
	draw_width, draw_height = get_frame_destination_size(frame_rect)
	return SCREEN_CENTER_X, SCREEN_CENTER_Y, draw_width, draw_height


def get_frame_destination_size(frame_rect):
	_, _, source_width, source_height = get_frame_source_rect(frame_rect)
	draw_height = MIN_DISPLAY_HEIGHT
	draw_width = round(draw_height * source_width / source_height)
	return draw_width, draw_height


def draw_frame(image, frame_rect):
	source_x, source_y, source_width, source_height = get_frame_source_rect(frame_rect)
	destination_x, destination_y, draw_width, draw_height = get_frame_destination_rect(frame_rect)
	image.clip_draw(
		source_x,
		source_y,
		source_width,
		source_height,
		destination_x,
		destination_y,
		draw_width,
		draw_height,
	)


def next_frame_index(frame_index, frame_count):
	return (frame_index + 1) % frame_count


def next_animation_index(animation_index, animation_count):
	if animation_count <= 0:
		raise ValueError("An animation sequence must not be empty")
	return (animation_index + 1) % animation_count


def advance_frame_time(
	frame_index, frame_timer, elapsed_time, frame_count, repeat_count=0, repeat_limit=None
):
	if frame_count <= 0:
		raise ValueError("An animation must contain at least one frame")
	if not math.isfinite(frame_timer) or not math.isfinite(elapsed_time):
		raise ValueError("Animation timing values must be finite")
	if repeat_limit is not None and repeat_limit <= 0:
		raise ValueError("Repeat limit must be positive")
	frame_timer += max(0.0, elapsed_time)
	finished = False
	while frame_timer + 1e-12 >= FRAME_DURATION and not finished:
		if (
			repeat_limit is not None
			and frame_index == frame_count - 1
			and repeat_count + 1 >= repeat_limit
		):
			repeat_count += 1
			frame_timer = 0.0
			finished = True
			break
		frame_index = next_frame_index(frame_index, frame_count)
		if frame_index == 0:
			repeat_count += 1
		frame_timer -= FRAME_DURATION
	frame_timer = max(0.0, frame_timer)
	return frame_index, frame_timer, repeat_count, finished


def is_pause_complete(pause_started_at, current_time):
	return current_time - pause_started_at >= PAUSE_DURATION


class AnimationSequence:
	def __init__(self, animation_frames=ANIMATION_FRAMES, animation_order=ANIMATION_ORDER):
		self.animation_frames = animation_frames
		self.animation_order = tuple(animation_order)
		if not self.animation_order or len(set(self.animation_order)) != len(self.animation_order):
			raise ValueError("Animation order must contain unique animation names")
		for name in self.animation_order:
			if name not in self.animation_frames or not self.animation_frames[name]:
				raise ValueError(f"Animation {name!r} has no frames")
			for frame_rect in self.animation_frames[name]:
				get_frame_source_rect(frame_rect)

		self.animation_index = 0
		self.frame_index = 0
		self.frame_timer = 0.0
		self.repeat_count = 0
		self.pause_started_at = None
		self.last_time = None

	@property
	def animation_name(self):
		return self.animation_order[self.animation_index]

	def update(self, current_time):
		if not math.isfinite(current_time):
			raise ValueError("Animation clock must return a finite time")
		elapsed_time = 0.0 if self.last_time is None else max(0.0, current_time - self.last_time)
		self.last_time = current_time

		if self.pause_started_at is not None:
			if is_pause_complete(self.pause_started_at, current_time):
				self.animation_index = next_animation_index(
					self.animation_index, len(self.animation_order)
				)
				self.frame_index = 0
				self.frame_timer = 0.0
				self.repeat_count = 0
				self.pause_started_at = None
		else:
			frames = self.animation_frames[self.animation_name]
			self.frame_index, self.frame_timer, self.repeat_count, finished = advance_frame_time(
				self.frame_index,
				self.frame_timer,
				elapsed_time,
				len(frames),
				self.repeat_count,
				REPEAT_LIMIT,
			)
			if finished:
				self.pause_started_at = current_time

		return self.animation_name, self.animation_frames[self.animation_name][self.frame_index]


def run():
	open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
	try:
		sprite_sheet = load_image(str(Path(__file__).with_name("AI_Sprite.png")))
		sequence = AnimationSequence()

		running = True
		while running:
			_, frame_rect = sequence.update(get_time())

			clear_canvas()
			draw_frame(sprite_sheet, frame_rect)
			update_canvas()

			for event in get_events():
				if event.type == SDL_QUIT:
					running = False

			delay(0.001)
	finally:
		close_canvas()


if __name__ == "__main__":
	run()
