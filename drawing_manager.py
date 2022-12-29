import sys
from pygame import Surface
from shapes import Shape, Circle, Ellipse
from singleton import Singleton
from typing import Iterable, List, Union


class DrawingManager(metaclass=Singleton):
    def initialize(self, drawing_surface: Surface):
        self.shapes: List[Shape] = []
        self.pixel = Surface((5, 5))
        self.pixel.fill("#123456")
        self.drawing_surface: Surface = drawing_surface
        self.drawing_surface_offset = (270, 80)
        self.rect = self.drawing_surface.get_rect(topleft=self.drawing_surface_offset)

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
                self.midpoint_circle_algorithm(shape.center, shape.radius)
            elif isinstance(shape, Ellipse):
                self.midpoint_ellipse_algorithm(shape.center, shape.xradius, shape.yradius)
                continue
            for i in range(-1, len(shape.vertices) - 1):
                self.bresenham(shape.vertices[i], shape.vertices[i + 1])

    def dda(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1
        inc = max(abs(dx), abs(dy))

        if inc == 0:
            return
        Xinc = dx / inc
        Yinc = dy / inc
        # print(dx, dy, Xinc, Yinc)
        x, y = x1, y1
        self.draw_to_surface(
            (
                round(x),
                round(y),
            ),
        )
        for i in range(inc):
            x += Xinc
            y += Yinc
            self.draw_to_surface(
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
            self.draw_to_surface((y1, x1))
        else:
            self.draw_to_surface((x1, y1))
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
                    self.draw_to_surface((x1, y1))
                    # self.drawing_surface.blit(self.pixel, (x1,y1))
                    pk = pk + 2 * dy
                else:

                    # (y1,x1) is passed in xt
                    # putpixel(y1, x1, YELLOW);
                    self.draw_to_surface((y1, x1))
                    # self.drawing_surface.blit(self.pixel, (y1,x1))
                    pk = pk + 2 * dy
            else:
                if y1 < y2:
                    y1 = y1 + 1
                else:
                    y1 = y1 - 1

                if lt_one_slope:
                    self.draw_to_surface((x1, y1))
                    # self.drawing_surface.blit(self.pixel, (x1,y1))
                else:
                    self.draw_to_surface((y1, x1))
                    # self.drawing_surface.blit(self.pixel, (y1,x1))
                pk = pk + 2 * dy - 2 * dx

    def midpoint_circle_algorithm(self, center, radius):
        x = radius
        y = 0
        x_center, y_center = center
        self.draw_to_surface((x + x_center, y + y_center))

        if radius > 0:  # if it's 0 then it's a single point
            # for the first point only 4 are enough,
            # because each two adjacent octents share a single point
            self.draw_to_surface((y + x_center, x + y_center))
            self.draw_to_surface((-x + x_center, y + y_center))
            self.draw_to_surface((-y + x_center, x + y_center))

        p = 1 - radius  # first decision parameter
        while x > y:
            # Y always gets incremented
            # as we are moving counter clock-wise from y=0 until y=x
            y += 1

            # check if point is inside or outside the circle
            if p <= 0:  # inside the circle or on the perimeter
                p = p + 2 * y + 1
            else:  # outside the circle
                x -= 1  # decrement x to move our pixels back inside the circle
                p = p + 2 * y - 2 * x + 1

            if (
                x < y
            ):  # we have to check here before drwaing since we just changed x and y
                return

            # draw the point on all 8 octents
            self.draw_to_surface((x + x_center, y + y_center))
            self.draw_to_surface((-x + x_center, y + y_center))
            self.draw_to_surface((x + x_center, -y + y_center))
            self.draw_to_surface((-x + x_center, -y + y_center))

            self.draw_to_surface((y + x_center, x + y_center))
            self.draw_to_surface((-y + x_center, x + y_center))
            self.draw_to_surface((y + x_center, -x + y_center))
            self.draw_to_surface((-y + x_center, -x + y_center))

    def midpoint_ellipse_algorithm(self, center, xradius, yradius):
        # Starting from Region1 -> starts from the y axis in the first quadrant
        x = 0
        y = yradius
        # a = rx, b = ry
        # d1 = (()) b**2 + 0.25*a**2 - a**2 * b
        d1 = (yradius**2) - (xradius**2) * yradius + (0.25 * xradius**2)

        dx = 2 * yradius**2 * x
        dy = 2 * xradius**2 * y

        while dx < dy:  # Region 1
            self.draw_to_surface((x + center[0], y + center[1]))
            self.draw_to_surface((-x + center[0], y + center[1]))
            self.draw_to_surface((x + center[0], -y + center[1]))
            self.draw_to_surface((-x + center[0], -y + center[1]))

            if d1 < 0:
                x += 1
                dx += (2 * yradius**2)
                d1 += dx + yradius**2
            else:
                x += 1
                y -= 1
                dx += 2 * yradius**2
                dy -= 2 * xradius**2
                d1 += dx - dy + yradius**2

        d2 = (
            (yradius**2 * (x + 0.5) ** 2)
            + (xradius**2 * (y - 1) ** 2)
            - (xradius**2 * yradius**2)
        )

        while y >= 0: #Second Region
            self.draw_to_surface((x + center[0], y + center[1]))
            self.draw_to_surface((-x + center[0], y + center[1]))
            self.draw_to_surface((x + center[0], -y + center[1]))
            self.draw_to_surface((-x + center[0], -y + center[1]))
        
            if d2 > 0:
                y -= 1
                dy -= 2 * xradius**2
                d2 += xradius**2 - dy
            else:
                y -= 1
                x += 1
                dx += 2 * yradius**2
                dy -= 2 * xradius**2
                d2 += dx -dy + xradius **2

    def check_collision_with_surface(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw_to_surface(self, position):
        x, y = position
        position = (
            x - self.drawing_surface_offset[0],
            y - self.drawing_surface_offset[1],
        )
        self.drawing_surface.blit(self.pixel, position)
