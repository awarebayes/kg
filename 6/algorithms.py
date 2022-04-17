from typing import List

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from my_types import Drawer, Point
from my_types import Edge, PixelColor
from lines import dda


def wait(delay):
    if delay != 0:
        QApplication.processEvents()
        QThread.msleep(delay)


def draw_edges(edges: List[Edge], drawer):
    for edge in edges:
        dda(edge.p1(), edge.p2(), drawer.pixel_edge)


def method_with_seed(edges: List[Edge], drawer: Drawer, seed_pixel: Point, delay: int):
    draw_edges(edges, drawer)
    stack = []

    stack.append(seed_pixel)  # записываем в стек затравочный пиксель

    while stack:
        point = stack.pop()
        x, y = point
        if drawer.canvas_y_low > y or drawer.canvas_y_high < y:
            continue

        wx = x  # запоминаем абсциссу

        # заполнение справа
        while drawer.check_color(x, y) != PixelColor.EDGE and x <= drawer.canvas_x_high:
            drawer.pixel_inside(x, y)
            x = x + 1

        xr = x - 1  # запоминаем пиксель справа

        x = wx

        # заполнение слева
        while drawer.check_color(x, y) != PixelColor.EDGE and x >= drawer.canvas_x_low:
            drawer.pixel_inside(x, y)
            x = x - 1

        xl = x + 1  # запоминаем пиксель слева

        x = xl
        y = y + 1

        # Ищем затравочные пиксели на строке выше
        while x <= xr:
            f = 0

            while (
                drawer.check_color(x, y) != PixelColor.EDGE
                and drawer.check_color(x, y) != PixelColor.FILL
                and x < xr
            ):
                if f == 0:
                    f = 1
                x = x + 1

            if f == 1:
                if (
                    x == xr
                    and drawer.check_color(x, y) != PixelColor.FILL
                    and drawer.check_color(x, y) != PixelColor.EDGE
                ):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                f = 0

            # Исследуем прерывание интервала
            wx = x
            while (
                drawer.check_color(x, y) == PixelColor.EDGE
                or drawer.check_color(x, y) == PixelColor.FILL
            ) and x < xr:
                x = x + 1

            if x == wx:
                x = x + 1

        x = xl
        y = y - 2

        # Ищем затравочные пиксели на строке ниже
        while x <= xr:
            f = 0

            while (
                drawer.check_color(x, y) != PixelColor.EDGE
                and drawer.check_color(x, y) != PixelColor.FILL
                and x < xr
            ):
                if f == 0:
                    f = 1
                x = x + 1

            if f == 1:
                if (
                    x == xr
                    and drawer.check_color(x, y) != PixelColor.FILL
                    and drawer.check_color(x, y) != PixelColor.EDGE
                ):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                f = 0

            # Исследуем прерывание интервала
            wx = x
            while (
                drawer.check_color(x, y) == PixelColor.EDGE
                or drawer.check_color(x, y) == PixelColor.FILL
            ) and x < xr:
                x = x + 1

            if x == wx:
                x = x + 1
        wait(delay)
