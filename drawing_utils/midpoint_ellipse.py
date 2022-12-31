
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