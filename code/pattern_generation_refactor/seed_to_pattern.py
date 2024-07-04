from seed_to_coordinate import *
from pattern_generator_cv2 import *
from graphics_cv2 import *

def seed_to_pattern(seed, output_file_name="output.png"):
    coordinate = seed_to_coordinate(seed)
    generate_vertices(6)
    draw_tiles(vertices_to_draw, coordinate, output_file_name)

seed_to_pattern(5)