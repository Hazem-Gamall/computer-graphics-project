from typing import Iterable

from pygame import Rect
from .shape import Shape

class Ellipse(Shape):
    SHAPE_INPUTS = 3

    def __init__(self) -> None:
        super().__init__()
        self.xradius = None
        self.yradius = None
        self.center = None

    def set_input(self, input):
        if self.input_counter == 0:
            self.center = input
            self.input_counter += 1
            self.vertices = [self.center]
            return False
        if self.input_counter == 1:
            self.input_counter +=1
            self.xradius = input
            return False
        else:
            self.input_counter +=1
            self.yradius = input
            return True

    def get_center(self) -> Iterable:
        return self.center
    
    def get_bounding_rect(self) -> Rect:
        return Rect(self.center[0] - self.xradius, self.center[1]-self.yradius, 2*self.xradius, 2*self.yradius)

if __name__ == "__main__":
    el = Ellipse()
    print(el)