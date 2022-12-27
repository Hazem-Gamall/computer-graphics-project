import math

from pygame import Rect
from .shape import Shape

class Rectangle(Shape):
    SHAPE_INPUTS = 2

    def __init__(self) -> None:
        super().__init__()
        self.top_left_vertex = None
        self.bottom_right_vertex = None

    def set_input(self, input):
        # print(self.input_counter)
        if self.input_counter == 0:
            self.top_left_vertex = input
            self.input_counter+=1
            return False
        else:
            self.bottom_right_vertex = input
            self.compute_vertices()
            return True


    def compute_vertices(self):
        x1,y1 = self.top_left_vertex
        x2,y2 = self.bottom_right_vertex
        width = (x2-x1)
        height = (y2-y1)
        top_right_vertex = (x1 + width, y1)
        bottom_left_vertex = (x1, y1+height)
        self.vertices = [self.top_left_vertex, top_right_vertex, self.bottom_right_vertex, bottom_left_vertex]

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
        self.rect = Rect(left, top, width, height)
        return self.rect

    def get_center(self):
        return self.rect.center
