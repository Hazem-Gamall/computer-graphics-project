
import sys


class Shape():
    SHAPE_INPUTS = None
    def __init__(self) -> None:
        self.vertices = []
        self.input_counter = 0
        self.num_of_inputs = self.SHAPE_INPUTS

    def set_input(self, input):
        print(self.input_counter)

        self.vertices.append(input)
        self.input_counter+=1
        print(self.vertices)
        if self.input_counter >= self.num_of_inputs:
            return True
        return False

class Line(Shape):
    SHAPE_INPUTS = 2

    

class Triangle(Shape):
    SHAPE_INPUTS = 3
    

class Rectangle(Shape):
    SHAPE_INPUTS = 2

    def __init__(self) -> None:
        super().__init__()
        self.top_left_vertex = None
        self.bottom_right_vertex = None

    def set_input(self, input):
        print(self.input_counter)
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