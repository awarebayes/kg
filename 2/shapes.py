from dataclasses import dataclass

import numpy as np
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QPolygonF
from math import pi, atan2
from transforms import apply_transform, get_translation_matrix

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

    def get_transforms(self):
        return self.transforms.get_composition()

    def get_base_points(self) -> np.ndarray:
        raise NotImplemented

    def after_get_base_points(self, points: np.ndarray) -> np.ndarray:
        return points

    def polygon(self):
        points = self.get_base_points()
        points = self.after_get_base_points(points)
        transform = self.get_transforms()
        points = apply_transform(transform, points)
        poly = QPolygonF([QPointF(*i) for i in points])
        return poly


@dataclass
class Circle(Drawable):
    x_0: float
    y_0: float
    r: float
    transforms: Transformations

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
        x = np.linspace(0, 1, int(dim * 2)) * k
        y = c - (x - d) ** 2

        x *= dim / k
        y *= dim / k

        points = np.vstack([x, y]).T
        return points

