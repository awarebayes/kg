from abc import ABC
from cmath import pi
from typing import Optional

import numpy as np


def get_translation_matrix(m, n):
    matrix = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [m, n, 1]])
    return matrix


def get_rotation_matrix(theta):
    matrix = np.array(
        [
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    return matrix


def get_scale_matrix(sx, sy):
    matrix = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]])
    return matrix


def apply_transform(transform, points):
    pad = np.ones((points.shape[0], 1))
    points = np.hstack([points, pad])
    transformed = points @ transform
    transformed = transformed[:, [0, 1]]
    return transformed


class BaseTransform(ABC):
    def get_transform(self, dim: float) -> np.ndarray:
        return np.eye(3)


def chain_transforms(dim, *transforms: BaseTransform):
    result = np.eye(3)
    for transform in transforms:
        result = result @ transform.get_transform(dim)
    return result


class TranslateTransform(BaseTransform):
    def __init__(self, trans_x, trans_y):
        self.trans_x = trans_x
        self.trans_y = trans_y

    def get_transform(self, dim):
        return get_translation_matrix(self.trans_x * dim, self.trans_y * dim)


class RotateTransform(BaseTransform):
    def __init__(self, deg):
        self.deg = deg

    def get_transform(self, dim):
        return get_rotation_matrix(self.deg * pi / 180)


class ScaleTransform(BaseTransform):
    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def get_transform(self, dim):
        return get_scale_matrix(self.sx, self.sy)


class TransformAroundPoint(BaseTransform):
    def __init__(self, point_x: float, point_y: float):
        self.go_to_point = TranslateTransform(-point_x, -point_y)
        self.transform: Optional[BaseTransform] = None
        self.come_from_point = TranslateTransform(point_x, point_y)

    def get_transform(self, dim):
        matrix = np.eye(3)
        matrix = matrix @ self.go_to_point.get_transform(dim)
        matrix = matrix @ self.transform.get_transform(dim)
        matrix = matrix @ self.come_from_point.get_transform(dim)
        return matrix


class RotateAroundPoint(TransformAroundPoint):
    def __init__(self, point_x: float, point_y: float, deg: float):
        super().__init__(point_x, point_y)
        self.transform = RotateTransform(deg)


class ScaleAroundPoint(TransformAroundPoint):
    def __init__(self, point_x: float, point_y: float, sx: float, sy: float):
        super().__init__(point_x, point_y)
        self.transform = ScaleTransform(sx, sy)
