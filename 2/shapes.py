from dataclasses import dataclass

import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF
from math import pi
from transforms import apply_transform

from model import Transformations


def get_unit_circle_points(n=100):
    theta = 2 * pi / n
    points = []

    for i in range(n):
        angle = theta * i
        points.append([np.cos(angle), np.sin(angle)])

    points = np.array(points)
    return points


class Drawable:
    transforms: Transformations
    dim: int

    def get_transforms(self):
        return self.transforms.get_composition()

    def get_base_points(self) -> np.ndarray:
        raise NotImplemented

    def after_get_base_points(self, points: np.ndarray) -> np.ndarray:
        return points

    def after_transform(self, points: np.ndarray) -> np.ndarray:
        return points

    def polygon(self):
        points = self.get_base_points()
        points = self.after_get_base_points(points)
        transform = self.get_transforms()
        points = apply_transform(transform, points)
        points = self.after_transform(points)
        poly = QPolygonF([QPointF(*i) for i in points])
        return poly


@dataclass
class Circle(Drawable):
    x_0: float
    y_0: float
    r: float
    transforms: Transformations
    dim: float

    def scale_translate_from_parameters(self, points):
        return points * self.r + np.array([self.x_0, self.y_0])

    def after_get_base_points(self, points: np.ndarray) -> np.ndarray:
        return self.scale_translate_from_parameters(points)

    def get_base_points(self) -> np.ndarray:
        return get_unit_circle_points(100)


@dataclass
class Parabola(Drawable):
    c: float
    d: float
    transforms: Transformations
    dim: float
    k: float = 10

    def get_base_points(self) -> np.ndarray:
        dim = self.dim
        k = self.k
        c = self.c / dim * k
        d = self.d / dim * k
        x = np.linspace(-0.5, 1.5, int(dim)) * k
        y = c - (x - d) ** 2

        x *= dim / k
        y *= dim / k

        points = np.vstack([x, y]).T
        return points

    def after_transform(self, points: np.ndarray) -> np.ndarray:
        points = points.tolist()

        edge_points = np.array([
            [9999, -9999],
            [-9999, -9999]
        ])
        rotated_edge = apply_transform(self.transforms.get_rotation_matrix(), edge_points)
        points.append(rotated_edge[0])
        points.append(rotated_edge[1])

        points = np.array(points)

        return points
