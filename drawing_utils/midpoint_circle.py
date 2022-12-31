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