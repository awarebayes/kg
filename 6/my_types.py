from dataclasses import dataclass
from typing import Tuple, Callable, DefaultDict
from enum import Enum

Point = Tuple[int, int]
TwoPointEdge = Tuple[Point, Point]


class PixelColor(Enum):
    FILL = 0
    EDGE = 1
    BACKGROUND = 2
    MARK = 3


@dataclass
class Edge:
    x1: float = 0
    y1: float = 0
    x2: float = 0
    y2: float = 0

    def min_x(self):
        return min(self.x1, self.x2)

    def min_y(self):
        return min(self.y1, self.y2)

    def max_x(self):
        return max(self.x1, self.x2)

    def max_y(self):
        return max(self.y1, self.y2)

    def p1(self):
        return self.x1, self.y1

    def p2(self):
        return self.x2, self.y2

    def __init__(self, x1, y1, x2, y2):
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2


def two_point_edge_to_edge(e: TwoPointEdge) -> Edge:
    return Edge(*e[0], *e[1])


@dataclass
class Drawer:
    _line_edge: Callable[[int, int, int, int], None]
    _line_inside: Callable[[int, int, int, int], None]
    _line_bg: Callable[[int, int, int, int], None]
    _line_mark: Callable[[int, int, int, int], None]
    buffer: DefaultDict[Tuple[int, int], PixelColor]
    canvas_x_low: int
    canvas_x_high: int
    canvas_y_low: int
    canvas_y_high: int

    def pixel_edge(self, x, y, intensity=255):
        self._line_edge(x, y, x, y)
        self.buffer[(x, y)] = PixelColor.EDGE

    def pixel_mark(self, x, y, intensity=255):
        self._line_mark(x, y, x, y)
        self.buffer[(x, y)] = PixelColor.MARK

    def pixel_inside(self, x, y, intensity=255):
        self._line_inside(x, y, x, y)
        self.buffer[(x, y)] = PixelColor.FILL

    def pixel_bg(self, x, y, intensity=255):
        self._line_bg(x, y, x, y)

    def check_color(self, x, y):
        return self.buffer[(x, y)]

    def pixel_not_edge_and_mark(self, x, y):
        pixel = self.buffer[(x, y)]
        return pixel != PixelColor.EDGE and pixel != PixelColor.MARK

    def pixel_not_edge_or_not_mark(self, x, y):
        pixel = self.buffer[(x, y)]
        return pixel != PixelColor.EDGE or pixel != PixelColor.MARK

    def pixel_is_edge_or_mark(self, x, y):
        pixel = self.buffer[(x, y)]
        return pixel == PixelColor.EDGE or pixel == PixelColor.MARK
