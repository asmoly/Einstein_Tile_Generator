import cv2
import numpy as np

from seed_to_coordinate import *
from geometry import Vector

OUTPUT_IMAGE_DIMENSIONS = Vector(500, 500)
SCALAR = 50

def draw_tile(tile, image, offset_coord=Vector(0, 0)):
    fill = tile[1]
    vertices = np.zeros((len(tile[0]), 2))
    
    for i in range (0, len(tile[0])):
        vertices[i][0] = tile[0][i].x*SCALAR - offset_coord.x*OUTPUT_IMAGE_DIMENSIONS.x
        vertices[i][1] = -tile[0][i].y*SCALAR + OUTPUT_IMAGE_DIMENSIONS.y + offset_coord.y*OUTPUT_IMAGE_DIMENSIONS.y

    vertices = vertices.astype(int)
    #vertices = vertices.reshape((-1, 1, 2))

    output_image = cv2.fillPoly(image, pts=[vertices], color=fill)
    output_image = cv2.polylines(image, [vertices], True, (0, 0, 0), 2)
    return output_image

def draw_tiles(tiles, offset_coord, output_file_name):
    output_image = np.full((OUTPUT_IMAGE_DIMENSIONS.y, OUTPUT_IMAGE_DIMENSIONS.x, 3), 255)

    for tile in tiles:
        output_image = draw_tile(tile, output_image, offset_coord=offset_coord)

    cv2.imwrite(output_file_name, output_image)