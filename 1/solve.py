from typing import Tuple, List

import numpy as np

from model import Point
from math import pi
from itertools import combinations

Triangle = Tuple[Point, Point, Point]


def l2(p1: Point, p2: Point) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def triangle_area(a: Point, b: Point, c: Point) -> float:
    return 1 / 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))


def triangle_sides(a, b, c) -> Tuple[float, float, float]:
    side_a = l2(b, c)
    side_b = l2(a, c)
    side_c = l2(a, b)
    return side_a, side_b, side_c


def triangle_peremeter(a, b, c):
    return sum(triangle_sides(a, b, c))


def curcumscribed_circle_radius(a: Point, b: Point, c: Point) -> float:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    s = 1 / 2 * (side_a + side_b + side_c)
    R = side_a * side_b * side_c / (4 * s * (s - side_a) * (s - side_b) * (s - side_c))
    assert R > 0
    return R


def inscribed_circle_radius(a: Point, b: Point, c: Point) -> float:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    s = 1 / 2 * (side_a + side_b + side_c)
    r = s * (s - side_a) * (s - side_b) * (s - side_c) / s
    assert r > 0
    return r


def inscribed_circle_center(a: Point, b: Point, c: Point) -> Point:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    p = triangle_peremeter(a, b, c)

    o_x = (a.x * side_a + b.x * side_b + c.x * side_c) / p
    o_y = (a.y * side_a + b.y * side_b + c.y * side_c) / p
    return Point(o_x, o_y)


def outscribed_circle_center(a: Point, b: Point, c: Point) -> Point:
    A_2 = l2(Point(0, 0), a) ** 2
    B_2 = l2(Point(0, 0), b) ** 2
    C_2 = l2(Point(0, 0), c) ** 2
    o_x = 1 / 2 * np.linalg.det([[A_2, a.y, 1], [B_2, b.y, 1], [C_2, c.y, 1]])
    o_y = 1 / 2 * np.linalg.det([[a.x, A_2, 1], [b.x, B_2, 1], [c.x, C_2, 1]])
    return Point(o_x, o_y)


def circle_area(r: float) -> float:
    return pi * r ** 2


def area_difference(triangle: Triangle) -> float:
    a, b, c = triangle
    R = curcumscribed_circle_radius(a, b, c)
    r = inscribed_circle_radius(a, b, c)
    diff = circle_area(R) - circle_area(r)
    assert diff > 0
    return diff


def is_triangle(triangle: Triangle) -> bool:
    a, b, c = triangle
    return abs((a.y - b.y) * (a.x - c.x) - (a.y - c.y) * (a.x - b.x)) > 0.0001


def triangle_with_max_circle_area_difference(points: List[Point]) -> Triangle:
    possible_triangles = filter(is_triangle, combinations(points, 3))
    answer = min(possible_triangles, key=area_difference, default=None)
    return answer
