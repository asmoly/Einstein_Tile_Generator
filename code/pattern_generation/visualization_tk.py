from pattern_generator import *
from graphics_tk import *

while True:
    next_generation()
    draw_tiles(vertices_to_draw, width=1000, height=1000)