from dataclasses import dataclass

import numpy as np
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QPolygonF
from math import pi, atan2
from numpy.linalg import norm

from numpy import sign
from scipy import spatial


from model import Transformations


@dataclass
class Circle:
    x_0: float
    y_0: float
    radius: float
    transforms: Transformations

    def apply_transforms(self, x_0, y_0, r):
        x_0 += self.transforms.trans_x
        y_0 += self.transforms.trans_y

        r *= self.transforms.scale

        return x_0, y_0, r

    def draw(self, qp: QPainter):
        x_0, y_0, r = self.apply_transforms(self.x_0, self.y_0, self.radius)
        x_0 = int(x_0)
        y_0 = int(y_0)
        r = int(r)

        pen = QPen(Qt.green)
        qp.setPen(pen)
        qp.drawEllipse(QPointF(x_0, y_0), r, r)
        qp.drawPoint(QPointF(x_0, y_0))


# https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm
def circle_intersection(p1, p2, center, r):
    Q = center  # Centre of circle
    V = p2 - p1  # Vector along line segment

    a = V.dot(V)
    b = 2 * V.dot(p1 - Q)
    c = p1.dot(p1) + Q.dot(Q) - 2 * p1.dot(Q) - r ** 2
    disc = b ** 2 - 4 * a * c
    if disc < 0:
        return None

    sqrt_disc = disc ** 0.5
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    t = max(0, min(1, - b / (2 * a)))

    return p1 + t * V


def find_intersection_bounds(mask, points):
    last_point = mask[0]
    intersection_bounds = []
    for i in range(len(mask)):
        if mask[i] != last_point:
            intersection_bounds.append((points[i-1], points[i]))
        last_point = mask[i]
    return intersection_bounds


def find_intersections(inside_mask, points, circle_center, r):
    intersection_bounds = find_intersection_bounds(inside_mask, points)
    intersections = []
    for bound in intersection_bounds:
        intersection = circle_intersection(*bound, circle_center, r)
        intersections.append(intersection)
    return intersections


def get_rotation_matrix(theta: float) -> np.ndarray:
    matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    return matrix


def angle_in_circle(circle_center, radius, point) -> float:
    non_rel = point - circle_center
    x, y = non_rel
    res = atan2(y, x)
    return res


def rotate_vector_around_point(vector: np.ndarray, point: np.ndarray, radians: float) -> np.ndarray:
    vector = vector - point
    rotation_matr = get_rotation_matrix(radians)
    vector = vector @ rotation_matr
    vector = vector + point
    return vector


def chord_path(circle_center, radius, p1, p2, n, choose_longest=False):
    start_angle = angle_in_circle(circle_center, radius, p1)
    end_angle = angle_in_circle(circle_center, radius, p2)

    if abs(end_angle - start_angle) > pi and not choose_longest:
        start_angle -= 2 * pi

    path = []

    theta = end_angle - start_angle
    d_theta = theta / n
    for i in range(n+1):
        angle = -d_theta * i
        new_point = rotate_vector_around_point(p1, circle_center, angle)

        path.append(new_point)
    path.append(p2)
    return path


def find_extrema(points):
    y_prev = points[0][1]
    for index, (x, y) in enumerate(points):
        if y_prev > y:
            return index
        y_prev = y
    raise ValueError("No extrema was found")


@dataclass
class Parabola:
    c: float
    d: float
    # центр круга
    x_0: float
    y_0: float
    # Размер изображения
    dim: float
    transforms: Transformations
    k: float = 10

    def get_coordinates(self):
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

    def apply_transforms(self, points: np.ndarray):

        # 1. идем к центру вращения
        center = np.asarray([self.x_0, self.y_0])

        points -= center

        # масштабируем в центре
        points *= self.transforms.scale

        # 2. вращаем вокруг центра вращения
        theta = self.transforms.rotate * pi / 180
        rotation_matrix = get_rotation_matrix(theta)
        points = points @ rotation_matrix

        # 3. идем обратно от центра вращения к исходным координатам
        points += center

        # 4. Переносим изображение
        translate = np.array([self.transforms.trans_x, self.transforms.trans_y])
        points += translate

        return points

    def draw(self, qp: QPainter):
        points = self.get_coordinates()

        points = self.apply_transforms(points)

        qp.setPen(QPen(Qt.blue))
        points = [QPointF(*i) for i in points]
        qp.drawPoints(*points)

    def draw_intersection(self, qp: QPainter, circle: Circle):
        points = self.get_coordinates()
        extrema_idx = find_extrema(points)
        points = self.apply_transforms(points)

        extrema = points[extrema_idx]

        # 1. поиск точек внутри окружности
        x_0 = circle.x_0 + self.transforms.trans_x
        y_0 = circle.y_0 + self.transforms.trans_y
        r = circle.radius * self.transforms.scale
        circle_center = np.array([x_0, y_0])
        extrema_outside = norm(circle_center - extrema) > r

        distance_to_circle_center = spatial.distance.cdist(points, [circle_center])

        inside_circle_mask = distance_to_circle_center < r
        inside_circle_mask = inside_circle_mask.T[0]

        # 1.1 внутри круга нет точек
        if not inside_circle_mask.any():
            return

        # 2. поиск точек пересечения с окружностью
        intersections = find_intersections(inside_circle_mask, points, circle_center, r)

        path = points[inside_circle_mask]
        points = path.tolist()

        qp.setPen(QPen(Qt.blue))
        path = QPainterPath()
        points = [QPointF(*i) for i in points]
        path.addPolygon(QPolygonF(points))
        qp.fillPath(path, Qt.blue)

        if len(intersections) == 2 and not extrema_outside:
            c_path = chord_path(circle_center, r, intersections[0], intersections[1], 100)
            path = QPainterPath()
            c_path = [QPointF(*i) for i in c_path]
            path.addPolygon(QPolygonF(c_path))
            qp.fillPath(path, Qt.red)

        if len(intersections) == 4:
            c_path_1 = chord_path(circle_center, r, intersections[0], intersections[3], 100)
            path = QPainterPath()
            c_path_1 = [QPointF(*i) for i in c_path_1]
            path.addPolygon(QPolygonF(c_path_1))
            qp.fillPath(path, Qt.red)

            c_path_2 = chord_path(circle_center, r, intersections[1], intersections[2], 100)
            path = QPainterPath()
            c_path_2 = [QPointF(*i) for i in c_path_2]
            path.addPolygon(QPolygonF(c_path_2))
            qp.fillPath(path, Qt.green)
