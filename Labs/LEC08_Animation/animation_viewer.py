from pico2d import SDL_QUIT, close_canvas, clear_canvas, get_events, open_canvas, update_canvas


def run():
	open_canvas(800, 600)

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
