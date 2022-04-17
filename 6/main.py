from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication

from my_gui import GuiMainWin
from my_types import Point


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)

        self.last_point: Optional[Point] = None
        self.first_point: Optional[Point] = None

        self.ui.add_btn.clicked.connect(self.add_point_button_clicked)
        self.ui.enclose_btn.clicked.connect(self.enclose)
        self.ui.clear_btn.clicked.connect(self.clear)
        self.ui.fill_btn.clicked.connect(self.fill)

    def add_point(self, x, y):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        if not 0 <= x <= width or not 0 <= y <= height:
            return

        self.ui.add_point(x, y)
        if self.last_point is not None:
            draw_func = self.ui.get_draw_edge_log()
            draw_func(*self.last_point, x, y)
        self.last_point = (x, y)

        if self.first_point is None:
            self.first_point = (x, y)

    def show_warning(self, message):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setInformativeText(message)
        box.exec()

    def enclose(self):
        if self.last_point is None or self.first_point is None:
            return self.show_warning("Первая точка не выбрана!")

        x, y = self.first_point
        self.add_point(x, y)
        self.last_point = None
        self.first_point = None

    def clear(self):
        self.first_point = None
        self.last_point = None
        self.ui.clear()

    def add_point_button_clicked(self):
        x = self.ui.x_inp.value()
        y = self.ui.y_inp.value()
        self.add_point(x, y)

    def fill(self):
        if self.first_point is not None or self.last_point is not None:
            return self.show_warning(
                "Фигура не замкнута! Нужно замыкать кнопочкой 'Замкнуть'!"
            )

        self.ui.fill()

    def mousePressEvent(self, event):
        shift_pressed = QApplication.queryKeyboardModifiers() == Qt.ShiftModifier
        print("shift:", shift_pressed)

        if event.button() == Qt.LeftButton and not shift_pressed:
            x, y = self.ui.transform(event.pos().x(), event.pos().y())
            self.add_point(x, y)

        elif event.button() == Qt.LeftButton and shift_pressed:
            if self.last_point is None:
                return

            x, y = self.ui.transform(event.pos().x(), event.pos().y())
            x, y = self.ui.get_ver_hor_line(x, y, self.last_point)

            self.ui.add_point(x, y)

            draw_func = self.ui.get_draw_edge_log()
            draw_func(*self.last_point, x, y)

            self.last_point = (x, y)

        elif event.button() == Qt.RightButton:
            x, y = self.ui.transform(event.pos().x(), event.pos().y())
            self.ui.set_seed(x, y)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWin()
    MainWindow.show()

    sys.exit(app.exec_())
