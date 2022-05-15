import sys
import win2
from algorithm import cyrus_beck_alg


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import (
    QBrush,
    QPen,
    QColor,
    QImage,
    QPixmap,
    QPainter,
    QPolygon,
    QTransform,
    QVector3D,
    QPolygonF,
)
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint, endl, QPointF
from math import sin, cos, pi, radians, fabs, floor

now = None
end_rect_ = False
ctrl = False
window = None

color_map = {
    'Красный': Qt.red,
    "Черный": Qt.black,
    "Белый": Qt.white,
    "Синий": Qt.blue,
    "Зеленый": Qt.green,
    "Желтый": Qt.yellow,
}

class Scene(QtWidgets.QGraphicsScene):
    def keyPressEvent(self, event):
        global ctrl
        # print(event.key() == Qt.Key_Control)
        if event.key() == Qt.Key_Control:
            # print("if")
            ctrl = True
        else:
            # print("else")
            ctrl = False
        # print("res", ctrl)

    # добавить точку по щелчку мыши
    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == Qt.LeftButton) and (end_rect_ == False):
            print("nenm")
            add_point(QMouseEvent.scenePos())

        if QMouseEvent.button() == Qt.RightButton:
            end_rect()


class Visual(QtWidgets.QMainWindow, win2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.scale(1, 1)
        h = self.graphicsView.height()
        w = self.graphicsView.width()
        self.scene = Scene(0, 0, w - 2, h - 2)
        self.scene.win = self
        self.graphicsView.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        # self.scene.setSceneRect(0, 0, w-2, h-2)
        self.pen_rest = QtGui.QPen(QtCore.Qt.black)
        self.pen_rest.setWidth(0)
        self.pen_line = QtGui.QPen(QtCore.Qt.green)
        self.pen_line.setWidth(0)
        self.pen_res = QtGui.QPen(QtCore.Qt.red)
        self.pen_res.setWidth(0)
        self.input_rect = False
        self.input_lines = True
        self.lines = []
        self.rect = []
        self.clip = None
        self.point_now = None
        self.color_back = QtCore.Qt.white

        self.radioButton_draw_line.clicked.connect(self.cheng)
        self.radioButton_draw_rest.clicked.connect(self.cheng)

        self.otsek_color.currentTextChanged.connect(self.change_otsecatel_color)
        self.otrezok_color.currentTextChanged.connect(self.change_otrezok_color)
        self.otsech_color.currentTextChanged.connect(self.change_otsechenie_color)

        self.pushButton_clean.clicked.connect(self.clean_screen)
        self.pushButton_draw_line.clicked.connect(self.add_line1)
        self.pushButton_draw_rest.clicked.connect(self.add_rect)
        self.pushButton_RES.clicked.connect(cirus)
        self.pushButton.clicked.connect(lambda: sys.exit(0))
        self.pushButton_draw_rest_2.clicked.connect(end_rect)

        self.change_otsecatel_color()
        self.change_otrezok_color()
        self.change_otsechenie_color()

    def cheng(self):
        global now, now_buf
        if self.radioButton_draw_line.isChecked():
            print(self.rect)
            now_buf = now
            now = None
            self.input_lines = True
            self.input_rect = False
        elif self.radioButton_draw_rest.isChecked():
            self.input_lines = False
            self.input_rect = True

    def clean_screen(self):
        global now
        self.scene.clear()
        self.lines = []
        self.rect = []
        now = None
        self.image.fill(Qt.white)
        r = self.table_line.rowCount()
        for i in range(r, -1, -1):
            self.table_line.removeRow(i)
        r = self.table_rust.rowCount()
        for i in range(r, -1, -1):
            self.table_rust.removeRow(i)

    def change_otrezok_color(self):
        color = color_map.get(self.otrezok_color.currentText(), Qt.black)
        self.pen_line.setColor(color)

    def change_otsecatel_color(self):
        color = color_map.get(self.otsek_color.currentText(), Qt.black)
        self.pen_rest.setColor(color)


    def change_otsechenie_color(self):
        color = color_map.get(self.otsech_color.currentText(), Qt.black)
        self.pen_res.setColor(color)


    # def set_black_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: black")
    #     self.color_back = QtCore.Qt.black

    # def set_white_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: white")
    #     self.color_back = QtCore.Qt.white

    # def set_blue_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: blue")
    #     self.color_back = QtCore.Qt.blue

    # def set_red_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: red")
    #     self.color_back = QtCore.Qt.red

    # def set_green_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: #00ff00")
    #     self.color_back = QtCore.Qt.green

    # def set_yellow_bg(self):
    #     self.graphicsView.setStyleSheet("background-color: yellow")
    #     self.color_back = QtCore.Qt.yellow

    def add_line1(self):
        try:
            x_start = float(self.lineEdit_5.text())
            x_end = float(self.lineEdit_8.text())
            y_start = float(self.lineEdit_6.text())
            y_end = float(self.lineEdit_7.text())
        except Exception:
            QMessageBox.warning(self, "Внимание!", "Неверно введены координаты!")
            return

        window.lines.append([[x_start, y_start], [x_end, y_end]])

        add_row(window, 1)
        i = window.table_line.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(x_start, y_start))
        item_e = QTableWidgetItem("[{0}, {1}]".format(x_end, y_end))
        window.table_line.setItem(i, 0, item_b)
        window.table_line.setItem(i, 1, item_e)
        window.scene.addLine(x_start, y_start, x_end, y_end, window.pen_line)
        window.point_now = None

    def add_rect(self):
        try:
            x = float(self.lineEdit_x.text())
            y = float(self.lineEdit_y.text())

        except Exception:
            QMessageBox.warning(self, "Внимание!", "Неверно введены координаты!")
            return

        add_point_simple(x, y)


# Добавить точку
def add_point_simple(x, y):
    global window, ctrl, now

    if (len(window.rect)) == 0:
        window.rect.append([x, y])

        add_row(window, 2)
        i = window.table_rust.rowCount() - 1
        item_b = QTableWidgetItem("{0}".format(x))
        item_e = QTableWidgetItem("{0}".format(y))
        window.table_rust.setItem(i, 0, item_b)
        window.table_rust.setItem(i, 1, item_e)

    else:
        add_row(window, 2)
        i = window.table_rust.rowCount() - 1
        item_b = QTableWidgetItem("{0}".format(x))
        item_e = QTableWidgetItem("{0}".format(y))
        print(item_b, item_e)
        window.table_rust.setItem(i, 0, item_b)
        window.table_rust.setItem(i, 1, item_e)

        i = len(window.rect)
        if ctrl:
            if abs(x - window.rect[i - 1][0]) < abs(y - window.rect[i - 1][1]):
                x = window.rect[i - 1][0]
            elif abs(y - window.rect[i - 1][1]) < abs(x - window.rect[i - 1][0]):
                y = window.rect[i - 1][1]
            ctrl = False
        window.scene.addLine(
            window.rect[i - 1][0], window.rect[i - 1][1], x, y, window.pen_rest
        )
        window.rect.append([x, y])


# Добавить строку с координатами с таблицу
def add_row(win, f):
    if f == 1:
        win.table_line.insertRow(win.table_line.rowCount())
    if f == 2:
        win.table_rust.insertRow(win.table_rust.rowCount())


# Добавить точку
def add_point(point):
    global window, ctrl, now
    x = point.x()
    y = point.y()

    if window.input_lines:
        if window.point_now is None:
            window.point_now = point
        else:
            if ctrl:
                if abs(point.x() - window.point_now.x()) < abs(
                    point.y() - window.point_now.y()
                ):
                    x = window.point_now.x()
                elif abs(point.y() - window.point_now.y()) < abs(
                    point.x() - window.point_now.x()
                ):
                    y = window.point_now.y()
                ctrl = False
            window.lines.append([[window.point_now.x(), window.point_now.y()], [x, y]])

            add_row(window, 1)
            i = window.table_line.rowCount() - 1
            item_b = QTableWidgetItem(
                "[{0}, {1}]".format(window.point_now.x(), window.point_now.y())
            )
            item_e = QTableWidgetItem("[{0}, {1}]".format(point.x(), point.y()))
            window.table_line.setItem(i, 0, item_b)
            window.table_line.setItem(i, 1, item_e)

            window.scene.addLine(
                window.point_now.x(), window.point_now.y(), x, y, window.pen_line
            )
            window.point_now = None

    if window.input_rect:
        if (len(window.rect)) == 0:
            window.rect.append([point.x(), point.y()])

            add_row(window, 2)
            i = window.table_rust.rowCount() - 1
            item_b = QTableWidgetItem("{0}".format(point.x()))
            item_e = QTableWidgetItem("{0}".format(point.y()))
            window.table_rust.setItem(i, 0, item_b)
            window.table_rust.setItem(i, 1, item_e)

        else:
            add_row(window, 2)
            i = window.table_rust.rowCount() - 1
            item_b = QTableWidgetItem("{0}".format(point.x()))
            item_e = QTableWidgetItem("{0}".format(point.y()))
            print(item_b, item_e)
            window.table_rust.setItem(i, 0, item_b)
            window.table_rust.setItem(i, 1, item_e)

            x = point.x()
            y = point.y()

            i = len(window.rect)
            if ctrl:
                if abs(point.x() - window.rect[i - 1][0]) < abs(
                    point.y() - window.rect[i - 1][1]
                ):
                    x = window.rect[i - 1][0]
                elif abs(point.y() - window.rect[i - 1][1]) < abs(
                    point.x() - window.rect[i - 1][0]
                ):
                    y = window.rect[i - 1][1]
                ctrl = False
            window.scene.addLine(
                window.rect[i - 1][0], window.rect[i - 1][1], x, y, window.pen_rest
            )
            window.rect.append([x, y])


def end_rect():
    global window, ctrl, now, end_rect_

    if window.input_rect:
        print("SSSSSSSSSSSSS", len(window.rect))
        if (len(window.rect)) == 0:
            QMessageBox.warning(
                window, "Внимание!", "Чтобы замкнуть, введите отсекатель!"
            )
        else:
            i = len(window.rect)
            window.scene.addLine(
                window.rect[i - 1][0],
                window.rect[i - 1][1],
                window.rect[0][0],
                window.rect[0][1],
                window.pen_rest,
            )


def all_polynom():
    p = QPolygonF()
    for i in window.rect:
        new_p = QPointF(i[0], i[1])
        p.append(new_p)

    pen = QPen(window.pen_rest.color())
    p_brush = QBrush(window.color_back)
    window.scene.addPolygon(p, pen, p_brush)


##############################################################


def draw_lines(arr):
    global window
    try:
        w = int(window.spinBox_w.text())
    except Exception:
        QMessageBox.warning(window, "Warning!", "Нецелое значение толщины!")
        return
    window.pen_res.setWidth(w)
    for l in arr:
        window.scene.addLine(l[1][0], l[1][1], l[0][0], l[0][1], window.pen_res)


def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()

def cirus():
    lines = cyrus_beck_alg(window.lines, window.rect)
    if lines:
       draw_lines(lines)

if __name__ == "__main__":
    main()
