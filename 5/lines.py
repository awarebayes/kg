from math import floor

from numpy import sign


def bresenham_integer(start, end, place_pixel):
    x_1, y_1 = start
    x_2, y_2 = end

    dx = abs(x_2 - x_1)
    dy = abs(y_2 - y_1)

    sign_dx = sign(x_2 - x_1)
    sign_dy = sign(y_2 - y_1)

    exchanged = False
    if dy > dx:
        dx, dy = dy, dx
        exchanged = True

    error = 2 * dy - dx
    x, y = x_1, y_1

    for _ in range(dx):
        place_pixel(x, y)
        if error >= 0:
            if exchanged:
                x += sign_dx
            else:
                y += sign_dy
            error -= 2 * dx
        if error <= 0:
            if exchanged:
                y += sign_dy
            else:
                x += sign_dx
            error += 2 * dy
