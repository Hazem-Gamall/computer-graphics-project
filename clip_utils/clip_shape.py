import sys
from typing import Tuple
from shapes import Rectangle, Shape, Line
from .cohen_sutherland import cohen_sutherland, get_region_code
from .liang_barsky import liang_barsky
from .clipper_algorithm import get_clipper_algorithm
# from shapes import Rectangle




def clip_shape(shape: Shape, window:Rectangle):
    post_clipping_shape_lines = []
    clipper = get_clipper_algorithm()
    for i in range(-1, len(shape.vertices)-1):
        new_points = clipper(shape.vertices[i], shape.vertices[i+1], window.max_p, window.min_p)
        if new_points:
            new_line = Line()
            new_line.set_input(new_points[0])
            new_line.set_input(new_points[1])
            post_clipping_shape_lines.append(new_line)

    return post_clipping_shape_lines
if __name__ == "__main__":
    p1 = (7,9)
    p2 = (11,4)
    window_max = (10,8)
    window_min = (4,4)
    print(bin(get_region_code(p2, window_max, window_min)))

    print(cohen_sutherland(p1,p2,window_max,window_min))