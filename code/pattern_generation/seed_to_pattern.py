import numpy as np

from pattern_generator import *
from graphics_cv2 import *
from geometry import Vector

# Converts a seed to coordinates so that you can get a unique piece of the pattern for each seed
# Each coordinate cooralates to a seed where the seed go clockwise starting in the top right going layer by layer
def seed_to_coordinate(seed):
    found_layer = False
    start_of_layer = 1

    layer = 0
    while found_layer == False:
        if seed >= start_of_layer and seed < start_of_layer + (4 + 8*layer):
            found_layer = True
        else:
            start_of_layer = start_of_layer + (4 + 8*layer)
            layer += 1

    number_of_coords_in_layer = 4 + layer*8

    output_coord = Vector(0, 0)

    # These if statements find the actual coordinates for the seed in the layer it found by checking where it is in the layer
    # This means the seed is in the right of the top row of the layer
    if seed >= start_of_layer and seed <= start_of_layer + layer:
        output_coord.y = layer
        output_coord.x = seed - start_of_layer
    # This is for when the seed is in the left of the top layer
    elif seed < start_of_layer + number_of_coords_in_layer and seed >= start_of_layer + number_of_coords_in_layer - layer - 1:
        output_coord.y = layer
        output_coord.x = seed - (start_of_layer + number_of_coords_in_layer)
    # This is for when the seed is in the bottom row of the layer
    elif seed > start_of_layer + layer*3 and seed <= start_of_layer + layer*5 + 2:
        output_coord.y = -layer - 1
        output_coord.x = (start_of_layer + layer*4 + 1) - seed
    # This is for if the seed is in the right column of the layer
    elif seed > start_of_layer + layer and seed <= start_of_layer + layer*3:
        output_coord.x = layer
        output_coord.y = (start_of_layer + layer*2) - seed
    # This is for if the seed is in the left column of the layer
    elif seed > start_of_layer + layer*5 + 2 and seed < start_of_layer + number_of_coords_in_layer - layer - 1:
        output_coord.x = -layer - 1
        output_coord.y = seed - (start_of_layer + layer*6 + 3)

    return output_coord

def seed_to_pattern(seed, output_file_name="output.png"):
    offset_coordinate = seed_to_coordinate(seed)
    next_generation()
    
    while True:
        output_image = np.full((OUTPUT_IMAGE_DIMENSIONS.y, OUTPUT_IMAGE_DIMENSIONS.x, 3), 255)
        for tile in vertices_to_draw:
            output_image = draw_tile(tile, output_image, offset_coord=offset_coordinate)

        if np.count_nonzero(output_image == 255) <= 9:
            finished_generating = True
            cv2.imwrite(output_file_name, output_image)
            return 0
        
        next_generation()

seed_to_pattern(6)
