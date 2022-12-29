import math
from typing import Iterable, Union
from pygame import Rect
from drawing_manager import DrawingManager

from shapes import Line, Shape
from shapes.rectangle import Rectangle
from clip_utils import get_region_code


def check_line_collision(line1: Iterable[Iterable], line2: Iterable[Iterable]):
    """Implements the technique described here
    http://paulbourke.net/geometry/pointlineplane/ by Paul Bourke"""

    (x1,y1),(x2,y2) = line1
    (x3,y3),(x4,y4) = line2

    denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))   
    if denominator == 0:
        return False
    ua = ( (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3) ) / denominator
    ub = ( (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3) ) / denominator

    if (ua >= 0 and ua <= 1) and (ub >= 0 and ub <= 1):
        return True
    return False

def check_line_inside_rectangle(line:Line, rectangle:Rectangle):
    p1_code = get_region_code(line.vertices[0], rectangle.max_p, rectangle.min_p)
    p2_code = get_region_code(line.vertices[1], rectangle.max_p, rectangle.min_p)
    return (p1_code == 0 and p2_code == 0)

def check_line_rectangle_collision(line: Line, rectangle:Rectangle):
    for i in range(-1, len(rectangle.vertices)-1):
        if check_line_collision(line.vertices, [rectangle.vertices[i], rectangle.vertices[i+1]]):
            return True
    
    #it's not really necessary to check if the line is inside the clipping window,
    #because we don't process it then anyway
    # return check_line_inside_rectangle(line, rectangle)
    return False

def check_shape_collision(shape1: Union[Shape,Line], shape2: Shape) -> bool:
    if type(shape1) == Line:
        return check_line_rectangle_collision(shape1, shape2)
    return shape1.get_bounding_rect().colliderect(shape2.get_bounding_rect())


def check_shape_point_collision(shape: Shape, point):

    if type(shape) == Line:
        return check_line_point_collision(shape, point)

    rect = shape.get_bounding_rect()
    if point[0] in range(rect.left, rect.right) and point[1] in range(
        rect.top, rect.bottom
    ):
        print(rect)
        print("collides")
        return True
    else:
        return False


def check_line_point_collision(line: Shape, point):
    """Using the technique described here
    https://www.jeffreythompson.org/collision-detection/line-point.php 
    by Jeffery Thompson"""
    # Calculate the length of the line
    # Calculate the distance between the point and each of the two ends of the line
    # if the sum of the two distances equals the length of the line then collision!
    ...
    line_length = math.dist(*line.vertices)
    line_width = DrawingManager().pixel.get_rect().width
    print("line length", line_length)
    point_distance1 = math.dist(point, line.vertices[0])
    point_distance2 = math.dist(point, line.vertices[1])
    point_distance_sum = point_distance1 + point_distance2
    print("ditsance sum", point_distance_sum)
    if int(point_distance_sum) in range(
        math.floor(line_length - line_width), math.ceil(line_length + line_width)
    ):
        return True
    return False
