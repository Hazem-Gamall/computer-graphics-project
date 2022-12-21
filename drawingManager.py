import sys
from pygame import Surface
from singleton import Singleton

class DrawingManager(metaclass=Singleton):

    def initialize(self, drawing_surface):
        self.shapes = []
        self.pixel = Surface((5,5))
        self.pixel.fill("#123456")
        self.drawing_surface:Surface = drawing_surface
        self.drawing_surface_offset = (270, 80)

    def register_shape(self, shape):
        self.shapes.append(shape)
    
    def draw(self):
        for shape in self.shapes:
            self.dda(*shape.vertices)

    def dda(self, p1, p2):
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]

        dx = x2-x1
        dy = y2-y1
        inc = max(abs(dx),abs(dy))
        Xinc = dx/inc
        Yinc = dy/inc
        print(dx, dy, Xinc, Yinc)
        x, y = x1, y1
        self.draw_to_screen(self.pixel, (round(x) - self.drawing_surface_offset[0], round(y)- self.drawing_surface_offset[1]))
        for i in range(inc):
            x += Xinc
            y += Yinc
            self.draw_to_screen(self.pixel, (round(x)- self.drawing_surface_offset[0], round(y)- self.drawing_surface_offset[1]))


    def draw_to_screen(self, surface, position):
        self.drawing_surface.blit(surface, position)
