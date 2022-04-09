from typing import List

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from my_types import Drawer
from my_types import Edge, PixelColor
from lines import bresenham_integer


def wait(delay):
    if delay != 0:
        QApplication.processEvents()
        QThread.msleep(delay)


def mark_border(edges_arr: List[Edge], drawer: Drawer):
    for line in edges_arr:
        if line.y2 == line.y1:
            continue

        y_max = line.max_y()
        y_min = line.min_y()

        dx = line.x2 - line.x1
        dy = line.y2 - line.y1

        y = y_min
        while y < y_max:
            x = dx / dy * (y - line.y1) + line.x1
            x_int = round(x)
            if drawer.check_color(x_int, y) == PixelColor.EDGE:
                drawer.pixel_edge(x_int + 1, y)
            else:
                drawer.pixel_edge(x_int, y)

            y += 1


def find_bounding_rect(edges: List[Edge]):
    min_x = min(map(Edge.min_x, edges))
    max_x = max(map(Edge.max_x, edges))

    min_y = min(map(Edge.min_y, edges))
    max_y = max(map(Edge.max_y, edges))
    return min_x, max_x, min_y, max_y


def fill_flag(edges: List[Edge], drawer: Drawer, delay: int):
    mark_border(edges, drawer)
    min_x, max_x, min_y, max_y = find_bounding_rect(edges)

    for y in range(min_y, max_y + 1):
        flag = False
        for x in range(min_x, max_x + 1):
            if drawer.check_color(x, y) == PixelColor.EDGE:
                flag = not flag
            if flag:
                drawer.pixel_inside(x, y)
        wait(delay)

    for edge in edges:
        bresenham_integer(edge.p1(), edge.p2(), drawer.pixel_edge)
