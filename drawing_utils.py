from typing import List
from logger import Logger

def dda(p1, p2) -> List:
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    points = []
    inc = max(abs(dx), abs(dy))

    if inc == 0:
        return
    Xinc = dx / inc
    Yinc = dy / inc
    # print(dx, dy, Xinc, Yinc)
    x, y = x1, y1
    points.append(
        (
            round(x),
            round(y),
        ),
    )
    for i in range(inc):
        x += Xinc
        y += Yinc
        points.append(
            (
                round(x),
                round(y),
            ),
        )

    return points

# aka midpoint
def bresenham(p1, p2, log=False) -> List : 

    # pk is initial decision making parameter
    # Note:x1&y1,x2&y2, dx&dy values are interchanged
    # and passed in plotPixel function so
    # it can handle both cases when m>1 & m<1
    # logger = Logger()
    data = {key:[] for key in ["x","y","p"]}

    x1, y1 = p1
    x2, y2 = p2
    lt_one_slope = True
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    points = []
    if dy > dx:  # slope > 1
        # print(x1, x2, dx, y1, y2, dy)
        x1, x2, dx, y1, y2, dy = y1, y2, dy, x1, x2, dx
        # print(x1, x2, dx, y1, y2, dy)
        lt_one_slope = False
        data["x"].append(y1)
        data["y"].append(x1)
        points.append((y1, x1))
    else:
        data["x"].append(x1)
        data["y"].append(y1)
        points.append((x1, y1))
    pk = 2 * dy - dx

    # for (int i = 0; i <= dx; i++) {
    for i in range(0, dx + 1):
        # print(x1, ",", y1)

        # checking either to decrement or increment the
        # value if we have to plot from (0,100) to (100,0)
        data["p"].append(pk)
        if x1 < x2:
            x1 = x1 + 1
        else:
            x1 = x1 - 1
        if pk < 0:

            # decision value will decide to plot
            # either  x1 or y1 in x's position
            if lt_one_slope:

                points.append((x1, y1))
                data["x"].append(x1)
                data["y"].append(y1)
                pk = pk + 2 * dy
            else:

                # (y1,x1) is passed in xt
                # putpixel(y1, x1, YELLOW);
                data["x"].append(y1)
                data["y"].append(x1)
                points.append((y1, x1))
                # self.drawing_surface.blit(self.pixel, (y1,x1))
                pk = pk + 2 * dy
        else:
            if y1 < y2:
                y1 = y1 + 1
            else:
                y1 = y1 - 1

            if lt_one_slope:
                data["x"].append(x1)
                data["y"].append(y1)
                points.append((x1, y1))
                # self.drawing_surface.blit(self.pixel, (x1,y1))
            else:
                data["x"].append(y1)
                data["y"].append(x1)
                points.append((y1, x1))
                # self.drawing_surface.blit(self.pixel, (y1,x1))
            pk = pk + 2 * dy - 2 * dx
    if log:
        return data
    return points

def midpoint_circle_algorithm(center, radius):
    x = radius
    y = 0
    x_center, y_center = center
    points = []
    points.append((x + x_center, y + y_center))

    if radius > 0:  # if it's 0 then it's a single point
        # for the first point only 4 are enough,
        # because each two adjacent octents share a single point
        points.append((y + x_center, x + y_center))
        points.append((-x + x_center, y + y_center))
        points.append((-y + x_center, x + y_center))

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
            return points

        # draw the point on all 8 octents
        points.append((x + x_center, y + y_center))
        points.append((-x + x_center, y + y_center))
        points.append((x + x_center, -y + y_center))
        points.append((-x + x_center, -y + y_center))

        points.append((y + x_center, x + y_center))
        points.append((-y + x_center, x + y_center))
        points.append((y + x_center, -x + y_center))
        points.append((-y + x_center, -x + y_center))
    return points

def midpoint_ellipse_algorithm(center, radius):
    # Starting from Region1 -> starts from the y axis in the first quadrant
    xradius, yradius = radius
    x = 0
    y = yradius
    # a = rx, b = ry
    # d1 = (()) b**2 + 0.25*a**2 - a**2 * b
    d1 = (yradius**2) - (xradius**2) * yradius + (0.25 * xradius**2)

    dx = 2 * yradius**2 * x
    dy = 2 * xradius**2 * y

    points = []

    while dx < dy:  # Region 1
        points.append((x + center[0], y + center[1]))
        points.append((-x + center[0], y + center[1]))
        points.append((x + center[0], -y + center[1]))
        points.append((-x + center[0], -y + center[1]))

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
        points.append((x + center[0], y + center[1]))
        points.append((-x + center[0], y + center[1]))
        points.append((x + center[0], -y + center[1]))
        points.append((-x + center[0], -y + center[1]))
    
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

    return points