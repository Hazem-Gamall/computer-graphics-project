import math

from pygame import Rect
from .shape import Shape

class Triangle(Shape):
    SHAPE_INPUTS = 3
    
    def get_bounding_rect(self):
        self.min_p = [math.inf]*2
        self.max_p = [-math.inf]*2
        for vertex in self.vertices:
            x,y = vertex
            self.min_p[0] = min(x, self.min_p[0])
            self.min_p[1] = min(y, self.min_p[1])

            self.max_p[0] = max(x, self.max_p[0])
            self.max_p[1] = max(y, self.max_p[1])
        left, top = self.min_p[0], self.min_p[1]
        width, height = self.max_p[0] - left, self.max_p[1] - top
        # print(left, width, height, )
        return Rect(left, top, width, height)

    def get_center(self):
        return ( (self.vertices[0][0] + self.vertices[1][0] + self.vertices[2][0])/3, (self.vertices[0][1] + self.vertices[1][1] + self.vertices[2][1])/3)
