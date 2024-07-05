import numpy as np

from pattern_generator import *
from graphics_cv2 import *

def seed_to_pattern(seed, output_file_name="output.png"):
    offset_coordinate = seed_to_coordinate(seed)
    next_generation()
    
    finished_generating = False

    while True:
        output_image = np.full((OUTPUT_IMAGE_DIMENSIONS.y, OUTPUT_IMAGE_DIMENSIONS.x, 3), 255)
        for tile in vertices_to_draw:
            output_image = draw_tile(tile, output_image, offset_coord=offset_coordinate)

        if np.count_nonzero(output_image == 255) <= 9:
            finished_generating = True
            cv2.imwrite(output_file_name, output_image)
            return 0
        
        next_generation()

seed_to_pattern(10)