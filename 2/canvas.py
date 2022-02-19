from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen, QPainterPath

from shapes import Circle, Parabola


class Canvas(QtWidgets.QFrame):
    def __init__(self, parent_widget, parent_view):
        super(Canvas, self).__init__(parent=parent_widget)
        self.setMinimumSize(QtCore.QSize(451, 461))
        self.setMouseTracking(True)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame")

        self.get_params = parent_view.controller.get_parameters
        self.get_transforms = parent_view.controller.get_transformations

    def paintEvent(self, event):
        self.redraw()

    def redraw(self):
        qp = QtGui.QPainter()
        qp.begin(self)
        params = self.get_params()
        transforms = self.get_transforms()
        size = self.size()
        size = size.width(), size.height()
        min_dim = min(size)

        qp.scale(1.0, -1.0)
        qp.translate(0, -min_dim)
        params.rescale(min_dim)
        transforms.rescale(min_dim)

        circle = Circle(x_0=params.a, y_0=params.b, r=params.r, transforms=transforms)
        circ_poly = circle.polygon()
        qp.setPen(QPen(Qt.blue))
        qp.drawPolygon(circ_poly)

        qp.setPen(QPen(Qt.red))
        qp.drawEllipse(QPointF(transforms.sr_center_x, transforms.sr_center_y), 5, 5)

        parabola = Parabola(c=params.c, d=params.d, transforms=transforms, dim=min_dim)
        parabola_poly = parabola.polygon()
        qp.drawPolygon(parabola_poly)

        intersection_poly = circ_poly.intersected(parabola_poly)
        path = QPainterPath()
        path.addPolygon(intersection_poly)
        qp.fillPath(path, Qt.blue)

        qp.end()


