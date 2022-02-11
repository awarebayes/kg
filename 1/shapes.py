from typing import List

from model import Point
import numpy as np
from abc import ABC, abstractmethod


class GeometryObject(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def scale(self, factor):
        pass

    @abstractmethod
    def translate(self, vec):
        pass

    @abstractmethod
    def aabb(self):
        pass


class Triangle(GeometryObject):
    def __init__(self, a: Point, b: Point, c: Point):
        super(Triangle, self).__init__()
        self.a = np.array([a.x, a.y])
        self.b = np.array([b.x, b.y])
        self.c = np.array([c.x, c.y])

    def scale(self, factor):
        self.a *= factor
        self.b *= factor
        self.c *= factor

    def translate(self, vec):
        self.a += vec
        self.b += vec
        self.c += vec

    def aabb(self):
        xs = self.a[0], self.b[0], self.c[0]
        ys = self.a[0], self.b[0], self.c[0]
        return np.array([min(xs), min(ys)]), np.array([max(xs), max(ys)])


class Circle(GeometryObject):
    def __init__(self, center: np.ndarray, radius: float):
        super(Circle, self).__init__()
        self.center = center
        self.radius = radius

    def scale(self, factor):
        self.radius *= factor

    def translate(self, vec):
        self.center += vec

    def aabb(self):
        return self.center - self.radius, self.center + self.radius


class ObjectComposition(GeometryObject):
    def __init__(self, objects: List[GeometryObject]):
        super(ObjectComposition, self).__init__()
        self.objects = objects

    def scale(self, factor):
        for o in self.objects:
            o.scale(factor)

    def translate(self, vec):
        for o in self.objects:
            o.translate(vec)

    def aabb(self):
        xs = []
        ys = []
        for o in self.objects:
            p1, p2 = o.aabb()
            xs += [p1[0], p2[0]]
            ys += [p1[1], p2[1]]

        return np.array([min(xs), min(ys)]), np.array([max(xs), max(ys)])
