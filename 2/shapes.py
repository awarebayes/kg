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


def angle_in_circle(circle_center, point) -> float:
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


def get_chord_angle_type(circle_center, parabola_inside_circle, p1, p2, qp):
    line_middle_point = (p1 + p2) / 2
    parabola_mean_point = parabola_inside_circle.mean(axis=0)

    line_normal = circle_center - line_middle_point
    parabola_normal = -(line_middle_point - parabola_mean_point)

    qp.drawEllipse(QPointF(*p1), 3, 3)
    qp.drawEllipse(QPointF(*p2), 3, 3)
    qp.drawLine(QPointF(*p1), QPointF(*p2))
    qp.drawLine(QPointF(*line_middle_point), QPointF(*(line_middle_point + parabola_normal)))
    qp.drawLine(QPointF(*line_middle_point), QPointF(*(line_middle_point + line_normal)))

    if line_normal @ parabola_normal > 0:
        print("Угол внутренний")
        return "внутренний"
    else:
        print("Угол внешний")
        return "внешний"


def chord_path(circle_center, radius, p1, p2, n, angle_type="внутренний"):
    start_angle = angle_in_circle(circle_center, p1)
    end_angle = angle_in_circle(circle_center, p2)

    # угол внешний, а нужно рисовать внутренний
    if abs(end_angle - start_angle) > pi and angle_type == "внутренний":
        start_angle += 2 * pi

    # угол внутренний, а нужно рисовать внешний
    if abs(end_angle - start_angle) < pi and angle_type == "внешний":
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


def check_circle_inside_parabola(circle_center, radius, parabola, degrees_rotated):
    theta = degrees_rotated * pi / 180
    rotate_backwards = get_rotation_matrix(-degrees_rotated)
    parabola = rotate_backwards @ parabola

    circle_start_x = circle_center[0] - radius
    circle_end_x = circle_center[0] + radius

    parabola_x = parabola[:, 0]
    parabola_clipped = parabola[parabola_x > circle_start_x & parabola_x < circle_end_x]

    # y = y_0 + sqrt(R^2 - (x-x_0)^2)
    circle_y = circle_center[1] + np.sqrt(radius ** 2 - (parabola_clipped[:, 0] - circle_center[0])**2)

    if (circle_y <= parabola_clipped[:, 1]).all():
        return True
    else:
        return False



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
        points = self.apply_transforms(points)

        # 1. поиск точек внутри окружности
        x_0 = circle.x_0 + self.transforms.trans_x
        y_0 = circle.y_0 + self.transforms.trans_y
        r = circle.radius * self.transforms.scale
        circle_center = np.array([x_0, y_0])

        distance_to_circle_center = spatial.distance.cdist(points, [circle_center])

        inside_circle_mask = distance_to_circle_center < r
        inside_circle_mask = inside_circle_mask.flatten()

        # 1.1 внутри круга нет точек
        if not inside_circle_mask.any():
            return

        # 2. поиск точек пересечения с окружностью
        intersections = find_intersections(inside_circle_mask, points, circle_center, r)

        path_arr = points[inside_circle_mask].tolist()
        path = QPainterPath()
        path_arr = [QPointF(*i) for i in path_arr]
        path.addPolygon(QPolygonF(path_arr))
        qp.fillPath(path, Qt.blue)

        if len(intersections) == 2:
            p1 = intersections[0]
            p2 = intersections[1]
            angle_type = get_chord_angle_type(circle_center, points[inside_circle_mask], p1, p2, qp)
            c_path = chord_path(circle_center, r, intersections[0], intersections[1], 100, angle_type)
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
