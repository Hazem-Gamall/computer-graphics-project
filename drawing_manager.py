import sys
from pygame import Surface
from shapes import Shape, Circle, Ellipse
from singleton import Singleton
from typing import Iterable, List, Union
from drawing_utils.line_drawer import get_line_drawer
import drawing_utils


class DrawingManager(metaclass=Singleton):
    def initialize(self, drawing_surface: Surface):
        self.shapes: List[Shape] = []
        self.pixel = Surface((5, 5))
        self.pixel.fill("#123456")
        self.drawing_surface: Surface = drawing_surface
        self.drawing_surface_offset = (270, 80)
        self.rect = self.drawing_surface.get_rect(topleft=self.drawing_surface_offset)
        self.line_drawer = get_line_drawer()

    def register_shapes(self, shapes: Union[Shape, Iterable]):
        if isinstance(shapes, Iterable):
            self.shapes += shapes
            return
        self.shapes.append(shapes)

    def pop_shape(self, shape: Shape):
        self.shapes.remove(shape)

    def draw(self):
        self.drawing_surface.fill("#A5C5E7")
        for shape in self.shapes:
            if isinstance(shape, Circle):
                points = drawing_utils.midpoint_circle_algorithm(shape.center, shape.radius)
            elif isinstance(shape, Ellipse):
                points = drawing_utils.midpoint_ellipse_algorithm(shape.center, shape.radius)
            else:
                points = []
                for i in range(-1, len(shape.vertices) - 1):
                    points += self.line_drawer(shape.vertices[i], shape.vertices[i + 1])
            
            self.draw_points_to_surface(points)


    def check_collision_with_surface(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw_points_to_surface(self, points):
        for point in points:
            self.draw_to_surface(point)

    def draw_to_surface(self, position):
        x, y = position
        position = (
            x - self.drawing_surface_offset[0],
            y - self.drawing_surface_offset[1],
        )
        self.drawing_surface.blit(self.pixel, position)
