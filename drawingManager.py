import sys
from pygame import Surface
from shapes import Shape
from singleton import Singleton
from typing import List

class DrawingManager(metaclass=Singleton):
    def initialize(self, drawing_surface: Surface):
        self.shapes:List[Shape] = []
        self.pixel = Surface((5, 5))
        self.pixel.fill("#123456")
        self.drawing_surface: Surface = drawing_surface
        self.drawing_surface_offset = (270, 80)
        self.rect = self.drawing_surface.get_rect(topleft = self.drawing_surface_offset)

    def register_shape(self, shape: Shape):
        self.shapes.append(shape)

    def draw(self):
        for shape in self.shapes:
            for i in range(-1, len(shape.vertices)-1):
                self.dda(shape.vertices[i], shape.vertices[i+1])

    def dda(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1
        inc = max(abs(dx), abs(dy))
        Xinc = dx / inc
        Yinc = dy / inc
        # print(dx, dy, Xinc, Yinc)
        x, y = x1, y1
        self.draw_to_surface(
            self.pixel,
            (
                round(x),
                round(y),
            ),
        )
        for i in range(inc):
            x += Xinc
            y += Yinc
            self.draw_to_surface(
                self.pixel,
                (
                    round(x),
                    round(y),
                ),
            )

    # aka midpoint
    def bresenham(self, p1, p2):

        # pk is initial decision making parameter
        # Note:x1&y1,x2&y2, dx&dy values are interchanged
        # and passed in plotPixel function so
        # it can handle both cases when m>1 & m<1
        x1, y1 = p1
        x2, y2 = p2
        lt_one_slope = True
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        if dy > dx:  # slope > 1
            # print(x1, x2, dx, y1, y2, dy)
            x1, x2, dx, y1, y2, dy = y1, y2, dy, x1, x2, dx
            # print(x1, x2, dx, y1, y2, dy)
            lt_one_slope = False
            self.draw_to_surface(self.pixel, (y1, x1))
        else:
            self.draw_to_surface(self.pixel, (x1, y1))
        pk = 2 * dy - dx

        # for (int i = 0; i <= dx; i++) {
        for i in range(0, dx + 1):
            # print(x1, ",", y1)

            # checking either to decrement or increment the
            # value if we have to plot from (0,100) to (100,0)
            if x1 < x2:
                x1 = x1 + 1
            else:
                x1 = x1 - 1
            if pk < 0:

                # decision value will decide to plot
                # either  x1 or y1 in x's position
                if lt_one_slope:

                    # putpixel(x1, y1, RED);
                    self.draw_to_surface(self.pixel, (x1, y1))
                    # self.drawing_surface.blit(self.pixel, (x1,y1))
                    pk = pk + 2 * dy
                else:

                    # (y1,x1) is passed in xt
                    # putpixel(y1, x1, YELLOW);
                    self.draw_to_surface(self.pixel, (y1, x1))
                    # self.drawing_surface.blit(self.pixel, (y1,x1))
                    pk = pk + 2 * dy
            else:
                if y1 < y2:
                    y1 = y1 + 1
                else:
                    y1 = y1 - 1

                if lt_one_slope:
                    self.draw_to_surface(self.pixel, (x1, y1))
                    # self.drawing_surface.blit(self.pixel, (x1,y1))
                else:
                    self.draw_to_surface(self.pixel, (y1, x1))
                    # self.drawing_surface.blit(self.pixel, (y1,x1))
                pk = pk + 2 * dy - 2 * dx
                
    def check_collision_with_surface(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print(self.rect)
            return True
        return False
    def draw_to_surface(self, surface_to_draw, position):
        x, y = position
        position = (x - self.drawing_surface_offset[0], y - self.drawing_surface_offset[1])
        self.drawing_surface.blit(surface_to_draw, position)
