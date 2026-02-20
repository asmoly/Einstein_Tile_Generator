import cv2
import numpy as np

from geometry import Vector

OUTPUT_IMAGE_DIMENSIONS = Vector(800, 800)
SCALAR = 50

def draw_tile(tile, image, offset_coord=Vector(0, 0)):
    fill = tile[1][1]
    # 确保 fill 是元组格式 (B, G, R)
    if isinstance(fill, list):
        fill = tuple(fill)
        
    vertices = np.zeros((len(tile[0]), 2))
    
    for i in range (0, len(tile[0])):
        vertices[i][0] = tile[0][i].x*SCALAR - offset_coord.x*OUTPUT_IMAGE_DIMENSIONS.x
        vertices[i][1] = tile[0][i].y*SCALAR + OUTPUT_IMAGE_DIMENSIONS.y + offset_coord.y*OUTPUT_IMAGE_DIMENSIONS.y

    # 显式转换为 int32，这是 OpenCV 最兼容的类型
    vertices = vertices.astype(np.int32) 

    # OpenCV 直接修改原图，不需要写 output_image = ...
    cv2.fillPoly(image, pts=[vertices], color=fill)
    cv2.polylines(image, [vertices], True, (0, 0, 0), 2)
    return image