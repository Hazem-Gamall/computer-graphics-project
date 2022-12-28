import sys
from typing import Tuple
from shapes import Rectangle, Shape, Line
# from shapes import Rectangle


TOP = 8
BOTTOM = 4
RIGHT = 2
LEFT = 1


def get_region_code(point, window_max, window_min):

    region_code = 0

    x, y = point
    if x < window_min[0]:
        region_code |= LEFT
    elif x > window_max[0]:
        region_code |= RIGHT

    #The next two are swapped because our cordinate system is mirrored
    if y < window_min[1]:
        region_code |= TOP
    elif y > window_max[1]:
        region_code |= BOTTOM

    return region_code
    

def cohen_sutherland(p1: Tuple, p2: Tuple, window_max: Tuple, window_min: Tuple) -> Tuple:
    
    xmax, ymax = window_max
    xmin, ymin = window_min

    while True:
        p1_code = get_region_code(p1, window_max, window_min)
        p2_code = get_region_code(p2, window_max, window_min)
        x1,y1 = p1
        x2, y2 = p2

        if p1_code == 0 and p2_code == 0:   #Trivial accept
            return p1, p2
        if p1_code&p2_code != 0:    #Trivial reject
            return None
        
        if p1_code != 0:
            outside_point_code = p1_code
        else:
            outside_point_code = p2_code

        if outside_point_code & TOP:    #Point on top of the window
            y = ymin    #not ymax because again, our coordinate system is mirrored
            x = x1 + ( (y-y1) * (x2-x1) ) /(y2-y1)
        elif outside_point_code & BOTTOM:   #Point beneath the window
            y = ymax    #same as above
            x = x1 + ( (y-y1) * (x2-x1) )/(y2-y1) #not (y-y1)/m because m=dy/dx and dx can be 0
        elif outside_point_code & RIGHT:    #Point to the right of the window
            x = xmax
            y = y1 + ( (y2-y1)*(x-x1) ) / (x2-x1)
        elif outside_point_code & LEFT:     #Point to the left of the window
            x = xmin
            y = y1 + ( (y2-y1)*(x-x1) ) / (x2-x1)
        

        if outside_point_code == p1_code:
            p1 = tuple(map(round, (x,y)))
        else:
            p2 = tuple(map(round, (x,y)))
        

def clip_shape(shape: Shape, window:Rectangle):
    post_clipping_shape_lines = []
    for i in range(-1, len(shape.vertices)-1):
        new_points = cohen_sutherland(shape.vertices[i], shape.vertices[i+1], window.max_p, window.min_p)
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