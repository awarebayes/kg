from dataclasses import dataclass

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from model import Transformations


@dataclass
class Circle:
    x_0: float
    y_0: float
    radius: float

    def apply_transforms(self, transformations: Transformations):
        #self.x_0 *= transformations.scale
        #self.y_0 *= transformations.scale

        self.x_0 += transformations.trans_x
        self.y_0 += transformations.trans_x

        self.radius *= transformations.scale

    def draw(self, qp: QPainter):
        x_0 = int(self.x_0)
        y_0 = int(self.y_0)
        r = int(self.radius)

        qp.drawEllipse(QPointF(x_0, y_0), r, r)


class Parabola:
    c: float
    d: float
