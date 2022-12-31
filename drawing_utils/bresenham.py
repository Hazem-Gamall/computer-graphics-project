
from typing import List

#aka midpoint
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
