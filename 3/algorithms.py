from math import floor
from numpy import sign


def dda(start, end, place_pixel):
    x_1, y_1 = start
    x_2, y_2 = end

    length = max(abs(x_2 - x_1), abs(y_2 - y_1))
    assert length > 0

    dx = (x_2 - x_1) / length
    dy = (y_2 - y_1) / length

    x = x_1  # + 0.5 * sign(dx)
    y = y_1  # + 0.5 * sign(dx)

    for i in range(0, length):
        place_pixel(round(x), round(y))
        x += dx
        y += dy


def bresenham_float(start, end, place_pixel):
    x_1, y_1 = start
    x_2, y_2 = end

    dx = abs(x_2 - x_1)
    dy = abs(y_2 - y_1)

    sign_dx = sign(x_2 - x_1)
    sign_dy = sign(y_2 - y_1)

    # обмен значений dx и dy в зависимости от углового коэфициета наклона отрезка
    exchanged = False
    if dy > dx:
        dx, dy = dy, dx
        exchanged = True

    error = dy / dx - 0.5
    x, y = x_1, y_1

    for _ in range(dx):
        place_pixel(x, y)
        if error >= 0:
            if exchanged:
                x += sign_dx
            else:
                y += sign_dy
            error -= 1
        if error <= 0:
            if exchanged:
                y += sign_dy
            else:
                x += sign_dx
            error += dy / dx

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


def bresenham_smooth(start, end, place_pixel, I=255):
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

    tan: float = dy / dx * I  # tan лежит в [0, 255]
    error: float = I / 2
    W: float = I - tan  # По идее будет в [-255, 255]
    x, y = x_1, y_1

    for _ in range(dx):
        place_pixel(x, y, intensity=round(error))
        if error < W:
            if exchanged:
                y += sign_dy
            else:
                x += sign_dx
            error += tan
        else:
            y += sign_dy
            x += sign_dx
            error -= W


def wu_x_line(start, end, place_pixel, i_max=255):
    x_1, y_1 = start
    x_2, y_2 = end

    if y_1 > y_2:
        x_1, y_1, x_2, y_2 = x_2, y_2, x_1, y_1

    dx = x_2 - x_1
    dy = y_2 - y_1
    tan = dx / dy

    x = x_1
    for y in range(y_1, y_2, 1):
        x_floor = floor(x)
        d_1 = x - x_floor
        d_2 = 1 - d_1
        int_1 = round(abs(d_1) * i_max)
        int_2 = round(abs(d_2) * i_max)

        place_pixel(x_floor, y, intensity=int_2)
        place_pixel(x_floor + 1, y, intensity=int_1)
        x += tan


def wu_y_line(start, end, place_pixel, i_max=255):
    x_1, y_1 = start
    x_2, y_2 = end

    if x_1 > x_2:
        x_1, y_1, x_2, y_2 = x_2, y_2, x_1, y_1

    dx = x_2 - x_1
    dy = y_2 - y_1
    tan = dy / dx

    y = y_1
    for x in range(x_1, x_2, 1):
        y_floor = floor(y)
        d_1 = y - y_floor
        d_2 = 1 - d_1
        int_1 = round(abs(d_1) * i_max)
        int_2 = round(abs(d_2) * i_max)

        place_pixel(x, y_floor, int_2)
        place_pixel(x, y_floor + 1, int_1)
        y += tan


def wu(start, end, place_pixel):
    x_1, y_1 = start
    x_2, y_2 = end

    dx = abs(x_2 - x_1)
    dy = abs(y_2 - y_1)

    if dx == 0:
        for y in range(min(y_1, y_2), max(y_1, y_2)):
            place_pixel(x_1, y)
    elif dy == 0:
        for x in range(min(x_1, x_2), max(x_1, x_2)):
            place_pixel(x, y_1)
    elif dy >= dx:
        wu_x_line(start, end, place_pixel)
    else:
        wu_y_line(start, end, place_pixel)


def draw_line(algorithm_name, start, end, place_pixel):
    algorithm = None
    if algorithm_name == "ЦДА":
        algorithm = dda
    elif algorithm_name == "Брезенхем":
        algorithm = bresenham_float
    elif algorithm_name == "Брезенхем Целочисленный":
        algorithm = bresenham_integer
    elif algorithm_name == "Брезенхем Сглаживание":
        algorithm = bresenham_smooth
    elif algorithm_name == "Ву":
        algorithm = wu

    algorithm(start, end, place_pixel)
