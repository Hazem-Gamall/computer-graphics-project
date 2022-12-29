from typing import Iterable

from pygame import Rect
from .shape import Shape

class Ellipse(Shape):
    SHAPE_INPUTS = 3

    def __init__(self) -> None:
        super().__init__()
        self.radius = []
        self.angle = 0
        self.center = None

    def set_input(self, input):
        if self.input_counter == 0:
            self.center = input
            self.input_counter += 1
            self.vertices = [self.center]
            return False
        if self.input_counter == 1:
            self.input_counter +=1
            self.radius.append(input)
            return False
        else:
            self.input_counter +=1
            self.radius.append(input)
            return True

    def get_center(self) -> Iterable:
        return self.center
    
    def get_bounding_rect(self) -> Rect:
        xradius, yradius = self.radius[0], self.radius[1]
        return Rect(self.center[0] - xradius, self.center[1]-yradius, 2*xradius, 2*yradius)

if __name__ == "__main__":
    el = Ellipse()
    print(el)