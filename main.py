import pyray as ray
from pyray import KeyboardKey
from vec2 import Vec2
from math import ceil
import random

ray.set_config_flags(ray.ConfigFlags.FLAG_WINDOW_RESIZABLE)
ray.init_window(800, 600, 'Infinite Sweeper')
ray.set_target_fps(360)

revealed_squares = set()
flagged_squares = set()
camera_pos = Vec2(0, 0)
seed = random.random()

square_size = 30

def is_mine(coord: Vec2) -> bool:
	# lmfao
	random.seed(str(coord) + str(seed))
	return random.random() < 0.2

def get_neighbors(coords: Vec2) -> list[Vec2]:
	return [
		coords + Vec2(-1,  1),
		coords + Vec2( 0,  1),
		coords + Vec2( 1,  1),
		coords + Vec2(-1,  0),
		coords + Vec2( 1,  0),
		coords + Vec2(-1, -1),
		coords + Vec2( 0, -1),
		coords + Vec2( 1, -1),
	]

def is_empty(coords: Vec2) -> bool:
	if coords.tuple not in revealed_squares: return False

	if is_mine(coords): return False

	return all(not is_mine(n) for n in get_neighbors(coords))

def count_mines(coords: Vec2) -> int:
	return sum(is_mine(n) for n in get_neighbors(coords))

def reveal_square(coords: Vec2) -> None:
	if coords.tuple in revealed_squares:
		return
	
	revealed_squares.add(coords.tuple)
	if is_empty(coords):
		for n in get_neighbors(coords):
			reveal_square(n)

def draw_square(coords: Vec2) -> None:
	screen_pos = coords * square_size - camera_pos

	ray.draw_rectangle(screen_pos.x, screen_pos.y, square_size, square_size, ray.GRAY)
	if coords.tuple in revealed_squares:
		if is_mine(coords):
			ray.draw_rectangle(screen_pos.x, screen_pos.y, square_size - 2, square_size - 2, ray.RED)
		else:
			ray.draw_rectangle(screen_pos.x, screen_pos.y, square_size - 2, square_size - 2, ray.LIGHTGRAY)
			if not is_empty(coords):
				ray.draw_text(str(count_mines(coords)), screen_pos.x + 8, screen_pos.y + 8, 16, ray.BLACK)
	else:
		ray.draw_rectangle(screen_pos.x, screen_pos.y, square_size - 4, square_size - 4, ray.WHITE)
		if coords.tuple in flagged_squares:
			ray.draw_rectangle(screen_pos.x + 4, screen_pos.y + 4, square_size - 8, square_size - 8, ray.RED)

while not ray.window_should_close():
	ray.begin_drawing()

	ray.clear_background(ray.WHITE)

	screen_width = ray.get_screen_width()
	screen_height = ray.get_screen_height()
	for x in range(camera_pos.x // square_size, ceil((camera_pos.x + screen_width) / square_size)):
		for y in range(camera_pos.y // square_size, ceil((camera_pos.y + screen_height) / square_size)):
			draw_square(Vec2(x, y))
	
	if ray.is_mouse_button_released(ray.MouseButton.MOUSE_BUTTON_LEFT):
		mouse_pos = ray.get_mouse_position()
		mouse_pos = Vec2(int(mouse_pos.x), int(mouse_pos.y))
		cell_pos = (mouse_pos + camera_pos) // square_size
		reveal_square(cell_pos)
	
	if ray.is_mouse_button_pressed(ray.MouseButton.MOUSE_BUTTON_RIGHT):
		mouse_pos = ray.get_mouse_position()
		mouse_pos = Vec2(int(mouse_pos.x), int(mouse_pos.y))
		cell_pos = (mouse_pos + camera_pos) // square_size
		if cell_pos in flagged_squares:
			flagged_squares.remove(cell_pos.tuple)
		else:
			flagged_squares.add(cell_pos.tuple)

	vel = Vec2(0, 0)
	if ray.is_key_down(KeyboardKey.KEY_RIGHT):
		vel.x += 1
	if ray.is_key_down(KeyboardKey.KEY_LEFT):
		vel.x -= 1
	if ray.is_key_down(KeyboardKey.KEY_UP):
		vel.y -= 1
	if ray.is_key_down(KeyboardKey.KEY_DOWN):
		vel.y += 1
	
	camera_pos += vel

	# ray.draw_text()

	ray.end_drawing()

ray.close_window()