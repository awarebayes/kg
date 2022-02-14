from typing import List, Dict

from model import Point
import numpy as np
from abc import ABC, abstractmethod
from copy import copy
from tkinter import Canvas


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

    @abstractmethod
    def draw(self, canvas: Canvas, **kwargs):
        pass


class Triangle(GeometryObject):
    def __init__(self, a: Point, b: Point, c: Point):
        super(Triangle, self).__init__()
        self.a = np.array([a.x, a.y])
        self.b = np.array([b.x, b.y])
        self.c = np.array([c.x, c.y])
        self.original_params = {
            "a": self.a.copy(),
            "b": self.b.copy(),
            "c": self.c.copy(),
        }
        self.point_names = {"a": "a", "b": "b", "c": "c"}

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
        ys = self.a[1], self.b[1], self.c[1]
        return np.array([min(xs), min(ys)]), np.array([max(xs), max(ys)])

    def draw(self, canvas: Canvas, **kwargs):
        canvas.create_line(*self.a, *self.b, **kwargs)
        canvas.create_line(*self.b, *self.c, **kwargs)
        canvas.create_line(*self.a, *self.c, **kwargs)
        self.annotate_point("a", canvas)
        self.annotate_point("b", canvas)
        self.annotate_point("c", canvas)

    def annotate_point(self, name: str, canvas: Canvas):
        center_orig = self.original_params[name]
        point = getattr(self, name)
        text = f"{self.point_names[name]} ({center_orig[0]:.2f}, {center_orig[1]:.2f})"
        canvas.create_text(*point, text=text, font=13)


class Circle(GeometryObject):
    def __init__(self, center: np.ndarray, radius: float):
        super(Circle, self).__init__()
        self.center = center
        self.radius = radius
        self.original_params = (center.copy(), radius)

    def scale(self, factor):
        self.radius *= factor
        self.center *= factor

    def translate(self, vec):
        self.center += vec

    def aabb(self):
        return self.center - self.radius, self.center + self.radius

    def draw(self, canvas: Canvas, **kwargs):
        p1, p2 = self.aabb()
        canvas.create_oval(*p1, *p2, **kwargs)
        self.annotate(canvas)

    def annotate(self, canvas: Canvas):
        center = self.original_params[0]
        text = (
            f"Circ ({center[0]:.2f}, {center[1]:.2f}) R: {self.original_params[1]:.2f}"
        )
        canvas.create_text(*self.center, text=text, font=13)


class ObjectComposition(GeometryObject):
    def __init__(self, objects: Dict[str, GeometryObject]):
        super(ObjectComposition, self).__init__()
        self.objects = objects

    def scale(self, factor):
        for o in self.objects.values():
            o.scale(factor)

    def translate(self, vec):
        for o in self.objects.values():
            o.translate(vec)

    def aabb(self):
        xs = []
        ys = []
        for o in self.objects.values():
            p1, p2 = o.aabb()
            xs += [p1[0], p2[0]]
            ys += [p1[1], p2[1]]

        return np.array([min(xs), min(ys)]), np.array([max(xs), max(ys)])

    def scale_to_canvas(self, canvas_dim):
        aabb_min, aabb_max = self.aabb()

        aabb_height = aabb_max[0] - aabb_min[0]
        aabb_width = aabb_max[1] - aabb_min[1]
        max_canvas_dim = max(canvas_dim)
        max_aabb_dim = max(aabb_height, aabb_width)

        scaling_coef = max_canvas_dim / max_aabb_dim
        scaling_coef *= 0.9

        self.scale(scaling_coef)

    def center(self):
        aabb_min, aabb_max = self.aabb()
        aabb_center = (aabb_max + aabb_min) / 2
        return aabb_center

    def translate_to_point(self, target_center):
        center_difference = target_center - self.center()
        self.translate(center_difference)

    def fit_to_canvas(self, canvas_dim):
        self.scale_to_canvas(canvas_dim)
        canvas_center = np.asarray(canvas_dim) / 2
        self.translate_to_point(canvas_center)

    def draw(self, canvas: Canvas, **kwargs):
        for o in self.objects.values():
            o.draw(canvas)

    def __getitem__(self, item: str) -> GeometryObject:
        return self.objects[item]
