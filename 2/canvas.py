import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen, QPainterPath

from shapes import Circle, Parabola
from transforms import chain_transforms, apply_transform


class Canvas(QtWidgets.QFrame):
    def __init__(self, parent_widget, parent_view):
        super(Canvas, self).__init__(parent=parent_widget)
        self.setMinimumSize(QtCore.QSize(451, 461))
        self.setMouseTracking(True)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame")

        self.get_params = parent_view.controller.get_parameters
        self.get_transform_array = parent_view.controller.get_transform_array
        self.get_sr_point = parent_view.controller.get_sr_point

    def paintEvent(self, event):
        self.redraw()

    def redraw(self):
        qp = QtGui.QPainter()
        qp.begin(self)
        params = self.get_params()
        sr_center = np.asarray(self.get_sr_point())
        size = self.size()
        size = size.width(), size.height()
        min_dim = min(size)

        qp.scale(1.0, -1.0)
        qp.translate(0, -min_dim)
        params.rescale(min_dim)

        transform_array = self.get_transform_array()
        transform_matrix = chain_transforms(min_dim, *transform_array)

        circle = Circle(
            x_0=params.a, y_0=params.b, r=params.r, dim=min_dim
        )
        circ_poly = circle.polygon(transform_matrix)
        qp.setPen(QPen(Qt.blue))
        qp.drawPolygon(circ_poly)


        sr_center = sr_center * min_dim
        qp.setPen(QPen(Qt.red))
        qp.drawEllipse(
            QPointF(*sr_center),
            5,
            5,
        )

        parabola = Parabola(c=params.c, d=params.d, dim=min_dim)
        parabola_poly = parabola.polygon(transform_matrix)
        qp.drawPolygon(parabola_poly)

        intersection_poly = circ_poly.intersected(parabola_poly)
        path = QPainterPath()
        path.addPolygon(intersection_poly)
        qp.fillPath(path, Qt.blue)

        qp.end()
