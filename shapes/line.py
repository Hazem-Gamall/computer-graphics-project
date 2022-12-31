from pygame import Rect
from line_drawer import get_line_drawer
from logger.logger import Logger
from .shape import Shape

class Line(Shape):
    SHAPE_INPUTS = 2

    def set_input(self, input):
        ret_val = super().set_input(input)
        if self.input_counter == 2:
            data = get_line_drawer()(*self.vertices, True)
            Logger().set_data(data)
            ...
        return ret_val


    def get_bounding_rect(self) -> Rect:
        ...

    def get_center(self):
        return ( (self.vertices[0][0] + self.vertices[1][0])/2, (self.vertices[0][1] + self.vertices[1][1])/2 )

    