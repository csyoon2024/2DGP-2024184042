from pico2d import SDL_QUIT, close_canvas, clear_canvas, get_events, open_canvas, update_canvas

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2


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
