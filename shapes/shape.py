from typing import Iterable
import math
from abc import ABCMeta, abstractmethod
from pygame import Rect


class ICollides(metaclass=ABCMeta):

    @abstractmethod
    def get_bounding_rect(self) -> Rect:
        ...

class Shape(ICollides, metaclass=ABCMeta):
    SHAPE_INPUTS = None
    def __init__(self) -> None:
        self.vertices = []
        self.input_counter = 0
        self.num_of_inputs = self.SHAPE_INPUTS

    def set_input(self, input):
        # print(self.input_counter)

        self.vertices.append(input)
        self.input_counter+=1
        # print(self.vertices)
        if self.input_counter >= self.num_of_inputs:
            return True
        return False

    @abstractmethod
    def get_center(self) -> Iterable:
        ...
        
    def __str__(self) -> str:
        return str(self.vertices)
    

