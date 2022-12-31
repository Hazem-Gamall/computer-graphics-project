

from typing import List


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
