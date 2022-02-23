import numpy as np


def get_translation_matrix(x, y):
    matrix = np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ])
    return matrix


def get_rotation_matrix(theta):
    matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])
    return matrix


def get_scale_matrix(sx, sy):
    matrix = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    return matrix


def apply_transform(transform, points):
    pad = np.ones((points.shape[0], 1))
    points = np.hstack([points, pad])
    transformed = transform @ points.T
    transformed = transformed[[0, 1], :].T
    return transformed


class BaseTransform:
    def get_transform(self):
        return np.eye(3)


class TranslateTransform:
    pass