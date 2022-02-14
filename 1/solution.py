from typing import Tuple, List, Iterator

import numpy as np

from model import Point
from math import pi
from itertools import combinations
import shapes

Triangle = Tuple[Point, Point, Point]


def l2(p1: Point, p2: Point) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def triangle_area(p1: Point, p2: Point, p3: Point) -> float:
    return (
        abs(
            p1.x * p2.y
            + p2.x * p3.y
            + p3.x * p1.y
            - p1.y * p2.x
            - p2.y * p3.x
            - p3.y * p1.x
        )
        / 2
    )


def triangle_sides(a, b, c) -> Tuple[float, float, float]:
    side_a = l2(b, c)
    side_b = l2(a, c)
    side_c = l2(a, b)
    return side_a, side_b, side_c


def triangle_peremeter(a, b, c):
    return sum(triangle_sides(a, b, c))


def outscribed_circle_radius(a: Point, b: Point, c: Point) -> float:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    area = triangle_area(a, b, c)
    R = side_a * side_b * side_c / (4 * area)
    assert R > 0
    return R


def inscribed_circle_radius(a: Point, b: Point, c: Point) -> float:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    s = (side_a + side_b + side_c) / 2
    r_2 = (s - side_a) * (s - side_b) * (s - side_c) / s
    return r_2**0.5


def inscribed_circle_center(a: Point, b: Point, c: Point) -> np.ndarray:
    side_a, side_b, side_c = triangle_sides(a, b, c)
    p = triangle_peremeter(a, b, c)

    o_x = (a.x * side_a + b.x * side_b + c.x * side_c) / p
    o_y = (a.y * side_a + b.y * side_b + c.y * side_c) / p
    return np.array([o_x, o_y])


def outscribed_circle_center(p1: Point, p2: Point, p3: Point) -> np.ndarray:

    a = np.linalg.det([[p1.x, p1.y, 1], [p2.x, p2.y, 1], [p3.x, p3.y, 1]])
    b_x = -np.linalg.det(
        [
            [p1.x**2 + p1.y**2, p1.y, 1],
            [p2.x**2 + p2.y**2, p2.y, 1],
            [p3.x**2 + p3.y**2, p3.y, 1],
        ]
    )

    b_y = np.linalg.det(
        [
            [p1.x**2 + p1.y**2, p1.x, 1],
            [p2.x**2 + p2.y**2, p2.x, 1],
            [p3.x**2 + p3.y**2, p3.x, 1],
        ]
    )

    o_x = -b_x / (2 * a)
    o_y = -b_y / (2 * a)

    return np.array([o_x, o_y])


def circle_area(r: float) -> float:
    return pi * r**2


def area_difference(triangle: Triangle) -> float:
    a, b, c = triangle
    R = outscribed_circle_radius(a, b, c)
    r = inscribed_circle_radius(a, b, c)
    diff = circle_area(R) - circle_area(r)
    assert diff > 0
    return diff


def is_triangle(triangle: Triangle) -> bool:
    a, b, c = triangle
    return abs((a.y - b.y) * (a.x - c.x) - (a.y - c.y) * (a.x - b.x)) > 0.0001


def triangles_iterator(points: List[Point]) -> Iterator[Triangle]:
    return filter(is_triangle, combinations(points, 3))


def triangle_with_max_circle_area_difference(points: List[Point]) -> Triangle:
    possible_triangles = triangles_iterator(points)
    answer = max(possible_triangles, key=area_difference, default=None)
    return answer


def get_shape_composition(triangle: Triangle) -> shapes.ObjectComposition:
    triangle_shape = shapes.Triangle(*triangle)
    triangle_shape.point_names = []
    in_center = inscribed_circle_center(*triangle)
    out_center = outscribed_circle_center(*triangle)

    in_r = inscribed_circle_radius(*triangle)
    out_r = outscribed_circle_radius(*triangle)

    in_circ_shape = shapes.Circle(in_center, in_r)
    out_circ_shape = shapes.Circle(out_center, out_r)

    return shapes.ObjectComposition(
        {
            "triangle": triangle_shape,
            "in_circ": in_circ_shape,
            "out_circ": out_circ_shape,
        }
    )
