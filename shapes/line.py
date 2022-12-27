from pygame import Rect
from .shape import Shape

class Line(Shape):
    SHAPE_INPUTS = 2

    def get_bounding_rect(self) -> Rect:
        ...

    def get_center(self):
        return ( (self.vertices[0][0] + self.vertices[1][0])/2, (self.vertices[0][1] + self.vertices[1][1])/2 )

    