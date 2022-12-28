from typing import Iterable
from pygame import Rect
from .shape import Shape

class Circle(Shape):
    SHAPE_INPUTS = 2 #center and radius
    def __init__(self) -> None:
        super().__init__()
        self.center = None
        self.radius = None
    
    def set_input(self, input):
        if self.input_counter == 0:
            self.center = input
            self.input_counter += 1
            return False
        self.radius = input
        self.input_counter += 1
        self.vertices = [self.center]
        return True
    
    def get_bounding_rect(self) -> Rect:
        return Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius*2, self.radius*2)
    
    def get_center(self) -> Iterable:
        return self.center
        

