from PyQt5 import QtCore, QtGui, QtWidgets
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
        transforms.rescale(min_dim)
        params.rescale(min_dim)

        circle = Circle(x_0=params.a, y_0=params.b, radius=params.r, transforms=transforms)
        circle.draw(qp)

        parabola = Parabola(c=params.c, d=params.d, x_0=params.a, y_0=params.b, transforms=transforms, dim=min_dim)
        parabola.draw(qp)
        parabola.draw_intersection(qp, circle)

        qp.end()


