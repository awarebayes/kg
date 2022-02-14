from PyQt5 import QtCore, QtGui, QtWidgets
from shapes import Circle


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

    def redraw_ignore_args(self, *args, **kwargs):
        self.redraw()

    def redraw(self):
        qp = QtGui.QPainter()
        qp.begin(self)
        params = self.get_params()
        transforms = self.get_transforms()
        size = self.size()
        size = size.width(), size.height()
        qp.scale(1.0, -1.0)
        qp.translate(0, -size[1])

        min_dim = min(size)
        transforms.rescale(min_dim)
        params.rescale(min_dim)

        circle = Circle(x_0=params.a, y_0=params.b, radius=params.r)
        circle.apply_transforms(transforms)
        circle.draw(qp)
        qp.end()


