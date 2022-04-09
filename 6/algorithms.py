from typing import List

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from my_types import Drawer, Point
from my_types import Edge, PixelColor
from lines import bresenham_integer, wu, dda


def wait(delay):
    if delay != 0:
        QApplication.processEvents()
        QThread.msleep(delay)


def draw_edges(edges: List[Edge], drawer):
    for edge in edges:
        wu(edge.p1(), edge.p2(), drawer.pixel_edge)


def method_with_seed(edges: List[Edge], drawer: Drawer, seed_pixel: Point, delay: int):
    draw_edges(edges, drawer)

    stack = [seed_pixel]

    while stack:

        seed_pixel = stack.pop()

        x = seed_pixel[0]
        y = seed_pixel[1]

        if y > drawer.canvas_y_high or y < drawer.canvas_y_low:
            continue

        drawer.pixel_mark(x, y)
        x_started = x
        y_started = y

        # заполняем интервал справа от затравки

        x += 1
        while (
            drawer.check_color(x, y) != PixelColor.MARK
            and drawer.check_color(x, y) != PixelColor.EDGE
            and x < drawer.canvas_x_high
        ):
            drawer.pixel_mark(x, y)
            x += 1

        x_right = x - 1

        # заполняем интервал слева от затравки

        x = x_started - 1
        while (
            drawer.check_color(x, y) != PixelColor.MARK
            and drawer.check_color(x, y) != PixelColor.EDGE
            and x > drawer.canvas_x_low
        ):
            drawer.pixel_mark(x, y)
            x -= 1

        x_left = x + 1

        # Проход по верхней строке

        x = x_left
        y = y_started + 1

        while x <= x_right:
            flag = False

            while (
                drawer.check_color(x, y) != PixelColor.MARK
                and drawer.check_color(x, y) != PixelColor.EDGE
                and x <= x_right
            ):
                flag = True
                x += 1

            # Помещаем в стек крайний справа пиксель

            if flag:
                if (
                    x == x_right
                    and drawer.check_color(x, y) != PixelColor.MARK
                    and drawer.check_color(x, y) != PixelColor.EDGE
                ):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])

                flag = False

            # Продолжаем проверку, если интервал был прерван

            x_beg = x
            while (
                drawer.check_color(x, y) == PixelColor.EDGE
                or drawer.check_color(x, y) == PixelColor.MARK
            ) and x < x_right:
                x = x + 1

            if x == x_beg:
                x += 1

        # Проход по нижней строке

        x = x_left
        y = y_started - 1

        while x <= x_right:
            flag = False

            while (
                drawer.check_color(x, y) != PixelColor.MARK
                and drawer.check_color(x, y) != PixelColor.EDGE
                and x <= x_right
            ):
                flag = True
                x += 1

            # Помещаем в стек крайний справа пиксель

            if flag:
                if (
                    x == x_right
                    and drawer.check_color(x, y) != PixelColor.MARK
                    and drawer.check_color(x, y) != PixelColor.EDGE
                ):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])

                flag = False

            # Продолжаем проверку, если интервал был прерван

            x_beg = x
            while (
                drawer.check_color(x, y) == PixelColor.EDGE
                or drawer.check_color(x, y) == PixelColor.MARK
                and x < x_right
            ):
                x = x + 1

            if x == x_beg:
                x += 1

        wait(delay)
