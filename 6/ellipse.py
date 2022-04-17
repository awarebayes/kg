import math


def method_middle_point_ellipse(x_center, y_center, a, b, place_pixel):
    a2, b2 = a**2, b**2
    ad, bd = 2 * a2, 2 * b2
    fp = b2 - a2 * b + 0.25 * a2
    x, y = 0, b

    dx, dy = b2, ad * y
    max_x = round(a2 * math.sqrt(1 / (b2 + a2)))
    while x <= max_x:
        place_pixel(x + x_center, y + y_center)
        place_pixel(-x + x_center, y + y_center)
        place_pixel(x + x_center, -y + y_center)
        place_pixel(-x + x_center, -y + y_center)

        x += 1
        if fp >= 0:
            y -= 1
            dy -= ad
            fp -= dy
        dx += bd
        fp += dx

    fp += 0.75 * (a2 - b2) - (a2 * y + b2 * x)
    dx, dy = bd * x, a2 * (2 * y - 1)
    while y >= 0:
        place_pixel(x + x_center, y + y_center)
        place_pixel(-x + x_center, y + y_center)
        place_pixel(x + x_center, -y + y_center)
        place_pixel(-x + x_center, -y + y_center)

        y -= 1
        if fp <= 0:
            x += 1
            dx += bd
            fp += dx
        dy -= ad
        fp -= dy
