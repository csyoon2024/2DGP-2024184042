from pico2d import SDL_QUIT, close_canvas, clear_canvas, get_events, open_canvas, update_canvas

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2
SPRITE_SHEET_WIDTH = 1792
SPRITE_SHEET_HEIGHT = 2358

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


def run():
	open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)

	running = True
	while running:
		clear_canvas()
		update_canvas()

		for event in get_events():
			if event.type == SDL_QUIT:
				running = False

	close_canvas()


if __name__ == "__main__":
	run()
