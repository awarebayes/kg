import sys
from copy import copy, deepcopy

import win2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
from math import sin, cos, pi, radians, fabs,  floor


from numpy import sign

now = None
now_buf = None
shift = False
wind = None

def bresenham(picture, x_start, xEnd, y_start, yEnd, color):
    if x_start == xEnd and y_start == yEnd:
        picture.addLine(x_start, y_start, x_start, y_start, color)
        return
    x_start = int(x_start)
    y_start = int(y_start)
    xEnd = int(xEnd)
    yEnd = int(yEnd)

    deltaX = xEnd - x_start
    deltaY = yEnd - y_start

    stepX = int(sign(deltaX))
    stepY = int(sign(deltaY))

    deltaX = abs(deltaX)
    deltaY = abs(deltaY)

    if deltaX <= deltaY:
        deltaX, deltaY = deltaY, deltaX
        flag = True
    else:
        flag = False

    acc = deltaY + deltaY - deltaX
    cur_x = x_start
    cur_y = y_start

    for i in range(deltaX + 1):
        picture.addLine(cur_x, cur_y, cur_x, cur_y, color)

        if acc >= 0:
            if flag:
                cur_x += stepX
            else:
                cur_y += stepY
            acc -= (deltaX + deltaX)
        if acc <= 0:
            if flag:
                cur_y += stepY
            else:
                cur_x += stepX
            acc += deltaY + deltaY


class Scene(QtWidgets.QGraphicsScene):
    
    def keyPressEvent(self, event):
        global shift
        if event.key() == Qt.Key_Shift:
            shift = True
        else:
            shift = False
        print("Shift pressed", shift)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        global shift
        if event.key() == Qt.Key_Shift:
            shift = False
        else:
            shift = True
        print("Shift released", shift)

    def mousePressEvent(self, event):
        add_point(event.scenePos())

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        global now
        if event.button() == Qt.MouseButton.LeftButton:
            now = None

    # добавить прямоугольник
    def mouseMoveEvent(self, event):
        global now, wind
        if wind.input_rect:
            if now is None:
                now = event.scenePos()
            else:
                wind.remove_otsekatel(self)
                p = event.scenePos()
                x1 = now.x()
                x2 = p.x()
                y1 = now.y()
                y2 = p.y()
                wind.rect_from_points((x1, x2), (y1, y2))
                wind.draw_otsekatel(self)
        strr = "Х левое = {0}\nХ правое = {1}\nУ нижнее = {2}\nУ верхнее = {3}\n".format(wind.rect[0],
                                                                                         wind.rect[1],
                                                                                         wind.rect[2],
                                                                                         wind.rect[3])
        wind.label_10.setText(strr)


color_russian_to_english = {
    "Белый": "white",
    "Черный": "black",
    "Желтый": "yellow",
    "Зеленый": "green",
    "Красный": "red",
    "Синий": "blue",
}

color_russian_to_qt = {
    "Белый": Qt.white,
    "Черный": Qt.black,
    "Желтый": Qt.yellow,
    "Зеленый": Qt.green,
    "Красный": Qt.red,
    "Синий": Qt.blue
}


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
        self.rect = [0, 0, 0, 0]
        self.clip = None
        self.point_now = None

        self.radioButton_draw_line.clicked.connect(self.cheng)
        self.radioButton_draw_rest.clicked.connect(self.cheng) 

        self.color_bg_select.currentTextChanged.connect(self.set_background)
        self.color_otrezok_select.currentTextChanged.connect(self.set_line_color)
        self.color_otsechenie_select.currentTextChanged.connect(self.set_otsechenie_color)
        self.color_otsekatel_selct.currentTextChanged.connect(self.set_otsekatel_color)

        self.pushButton_clean.clicked.connect(self.clean_screen)
        self.pushButton_draw_line.clicked.connect(self.add_line1)
        self.pushButton_draw_rest.clicked.connect(self.add_rect)
        # self.pushButton_gran.clicked.connect(self.add_bars)
        self.pushButton_RES.clicked.connect(clipping)
        self.edges_button.clicked.connect(self.draw_edges)
        self.exitButton.clicked.connect(lambda: exit(0))
        self.graphicsView.setFocus()


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
        # self.table_line.clear()
        self.lines = []
        now = None
        self.image.fill(Qt.white)
        r = self.table_line.rowCount()
        for i in range(r, -1, -1):
            self.table_line.removeRow(i)

    def set_line_color(self):
        text = self.color_otrezok_select.currentText()
        color = color_russian_to_qt[text]
        self.pen_line.setColor(color)

    def set_otsechenie_color(self):
        text = self.color_otsechenie_select.currentText()
        color = color_russian_to_qt[text]
        self.pen_res.setColor(color)

    def set_otsekatel_color(self):
        text = self.color_otsekatel_selct.currentText()
        color = color_russian_to_qt[text]
        self.pen_rest.setColor(color)

    def set_background(self):
        color_text = self.color_bg_select.currentText()
        bg_color = color_russian_to_english[color_text]
        self.graphicsView.setStyleSheet(f"background-color: {bg_color}")


    def add_line1(self):
        try:
            x_start = float(self.lineEdit_5.text())
            x_end = float(self.lineEdit_8.text())
            y_start = float(self.lineEdit_6.text())
            y_end = float(self.lineEdit_7.text())
        except Exception:
            QMessageBox.warning(self, "Внимание!", "Неверно введены координаты!")
            return

        self.scene_add_line(x_start, x_end, y_start, y_end)

    def scene_add_line(self, x_start, x_end, y_start, y_end):
        wind.lines.append([[x_start, y_start],
                           [x_end, y_end]])

        add_row(wind)
        i = wind.table_line.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(x_start, y_start))
        item_e = QTableWidgetItem("[{0}, {1}]".format(x_end, y_end))
        wind.table_line.setItem(i, 0, item_b)
        wind.table_line.setItem(i, 1, item_e)

        # bresenham(wind.scene, x_start, x_end, y_start, y_end, wind.pen_line)
        wind.scene.addLine(x_start, y_start, x_end, y_end, wind.pen_line)
        wind.point_now = None

    def add_rect(self):
        global now
        try:
            x_left = float(self.lineEdit_xleft.text())
            x_right = float(self.lineEdit_xright.text())
            y_down = float(self.lineEdit_ydown.text())
            y_up = float(self.lineEdit_yup.text())
        except Exception:
            QMessageBox.warning(self, "Внимание!", "Неверно введены координаты!")
            return
        self.remove_otsekatel(self.scene)
        now = QtCore.QPointF(x_left, y_up)
        # print(now, type(now))
        self.rect_from_points((x_left, x_right), (y_down, y_up))

        strr = "Х левое = {0}\nХ правое = {1}\nУ нижнее = {2}\nУ верхнее = {3}\n".format(x_left, x_right, y_down, y_up)
        self.label_10.setText(strr)

        self.scene.addRect(x_left, y_up, abs(x_right - x_left), abs(y_down - y_up), self.pen_rest)
        print("NOW", now)

    def rect_from_points(self, xs, ys):
        self.rect[0] = min(xs)
        self.rect[1] = max(xs)
        self.rect[2] = min(ys)
        self.rect[3] = max(ys)

    def draw_otsekatel(self, scene):
        x1 = self.rect[0]
        y1 = self.rect[2]
        dx = self.rect[1] - self.rect[0]
        dy = self.rect[3] - self.rect[2]
        scene.addRect(x1, y1, dx, dy, self.pen_rest)

    def remove_otsekatel(self, scene):
        x1 = self.rect[0]
        y1 = self.rect[2]
        scene.removeItem(scene.itemAt(x1, y1, QTransform()))

    def draw_edges(self):
        global now, wind
        if self.rect == [0, 0, 0, 0]:
            QMessageBox.warning(self, "Внимание!", "Не введен отсекатель!")
        else:
            x1 = self.rect[0]
            y1 = self.rect[2]
            x2 = self.rect[1]
            y2 = self.rect[3]

            k = 0.2
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            # задаем граничные отрезки
            self.scene_add_line(x1 + dx * k, x2 - dx * k, y1, y1)
            self.scene_add_line(x1 + dx * k, x2 - dx * k, y2, y2)
            self.scene_add_line(x1, x1, y1 + dy * k, y2 - dy * k)
            self.scene_add_line(x2, x2, y1 + dy * k, y2 - dy * k)



# Добавить строку с координатами с таблицу
def add_row(win):
    win.table_line.insertRow(win.table_line.rowCount())

# Добавить точку
def add_point(point):
    global wind, shift
    print("add_point, shift", shift)
    x = point.x()
    y = point.y()
    print("x, y", x, y)
    if wind.input_lines:
        if wind.point_now is None:
            wind.point_now = point
        else:
            if shift:
                if abs(point.x() - wind.point_now.x()) < abs(point.y() - wind.point_now.y()):
                    x = wind.point_now.x()
                elif abs(point.y() - wind.point_now.y()) < abs(point.x() - wind.point_now.x()):
                    y = wind.point_now.y()
                # shift = False

            wind.lines.append([[wind.point_now.x(), wind.point_now.y()],
                            [x, y]])

            add_row(wind)
            i = wind.table_line.rowCount() - 1
            item_b = QTableWidgetItem("[{0}, {1}]".format(wind.point_now.x(), wind.point_now.y()))
            item_e = QTableWidgetItem("[{0}, {1}]".format(x, y))
            wind.table_line.setItem(i, 0, item_b)
            wind.table_line.setItem(i, 1, item_e)
            # bresenham(wind.scene, wind.point_now.x(), x, wind.point_now.y(), y, wind.pen_line)
            wind.scene.addLine(wind.point_now.x(), wind.point_now.y(), x, y, wind.pen_line)
            wind.point_now = None


def get_code(a, rect):
    # rect = [Х левый, Х правый, У нижнее, У верхнее]
    code = [0, 0, 0, 0]
    if a[0] < rect[0]: # X < X левый
        code[0] = 1
    if a[0] > rect[1]: # X > X правый
        code[1] = 1
    if a[1] > rect[2]: # У < У верхнее
        code[2] = 1
    if a[1] < rect[3]: # У > У нижнее
        code[3] = 1

    return code

# Отсечение!!!
# Отсечение производится в определенном порядке:
# левой, правой, нижней, верхней границами отсекателя.
def clipping():
    global wind
    try:
        w = int(wind.spinBox_w.text())
    except Exception:
        QMessageBox.warning(wind, "Внимание!", "Нецелое значение толщины!")
        return 
    wind.pen_res.setWidth(w)

    # if now is not None:
    #     buf = wind.scene.itemAt(now.x(), now.y(), QTransform())
    #     if buf is None:
    #         QMessageBox.warning(wind, "Внимание!", "Не введен отсекатель!")
    #     else:
    #         buf = buf.rect()
    #         wind.clip = [buf.left(), buf.right(), buf.top(),  buf.bottom()]
    #     # buf = wind.scene.itemAt(now, QTransform()).rect()
    #     wind.clip = [buf.left(), buf.right(), buf.top(),  buf.bottom()]
    # else:
    #     QMessageBox.warning(wind, "Внимание!", "111Не введен отсекатель!")
    #     return

    rect = wind.rect[:]
    rect[3], rect[2] = rect[2], rect[3]
    lines = deepcopy(wind.lines)
    for b in wind.lines[:]:
        cohen_sutherland(b, rect)
    wind.lines = lines

def log_prod(code1, code2):
    p = 0
    for i in range(4):
        p += code1[i] & code2[i]

    return p

#  Видимость
def is_visible(bar, rect):
    """Видимость - 0 = невидимый
                   1 = видимый
                   2 = частично видимый"""
    # вычисление кодов концевых точек отрезка
    s1 = sum(get_code(bar[0], rect))
    s2 = sum(get_code(bar[1], rect))

    # предположим, что отрезок частично видим
    vis = 2

    # проверка полной видимости отрезка
    if not s1 and not s2:
        vis = 1
    else:
        # проверка тривиальной невидимости отрезка
        l = log_prod(get_code(bar[0], rect), get_code(bar[1], rect))
        if l != 0:
            vis = 0

    return vis


def cohen_sutherland(bar, rect):
    global wind
    # инициализация флага
    flag = 0 # общего положения
    m = 1

    # проверка вертикальности и горизонтальности отрезка
    if bar[1][0] - bar[0][0] == 0:
        flag = -1   # вертикальный отрезок
    else:
        # вычисление наклона
        m = (bar[1][1] - bar[0][1]) / (bar[1][0] - bar[0][0])
        if m == 0:
            flag = 1   # горизонтальный

    # для каждой стороны окна
    # Когда у нас вертикаль - то пропускается i = 0 и i = 1 
    # Когда у нас горизонталь - то пропускаем i = 3 и i = 4
    for i in range(4):
        """Видимость - 0 = невидимый
                       1 = видимый
                       2 = частично видимый"""
        # Опредление видимости
        vis = is_visible(bar, rect)
        # Если тривиально видим (полностью видим), то рисуем и выходим из цикла
        if vis == 1:
            print("if vis == 1:")
            # bresenham(wind.scene, bar[0][0], bar[1][0], bar[0][1], bar[1][1], wind.pen_res)
            wind.scene.addLine(bar[0][0], bar[0][1], bar[1][0], bar[1][1], wind.pen_res)
            return
        # Иначе проверяем на невидимость (тривиальную невидимость), 
        # то выход из цикла
        elif not vis:
            print("if vis == 1: else")
            return

        # проверка пересечения отрезка и стороны окна
        code1 = get_code(bar[0], rect)
        code2 = get_code(bar[1], rect)

        # Если Т1 == Т2, то переход на след шаг цикла
        if code1[i] == code2[i]:
            print("if code1[i] == code2[i]:")
            continue

        
        # проверка нахождения Р1 вне окна; если Р1 внутри окна, 
        # то Р2 и Р1 поменять местами
        # Если Т1 == 0, то обмен местами точек, 
        # (так как мы всегда принимаем Р1 за невидимую)
        if not code1[i]:
            print("f not code1[i]:")
            bar[0], bar[1] = bar[1], bar[0]


        # поиск пересечений отрезка со сторонами окна
        # Проверка  вертикальности  отрезка:  если Fl =-1, то переход к bar[0][1] = rect[i]
        if flag != -1:
            print("if flag != -1:")
            # СРавниваем i с 2, так как счет с 0
            if i < 2:
                print("if flag != -1: if i < 2")
                bar[0][1] = m * (rect[i] - bar[0][0]) + bar[0][1]
                bar[0][0] = rect[i]
                continue
            else:
                print("if flag != -1: if i < 2 else")
                bar[0][0] = (1 / m) * (rect[i] - bar[0][1]) + bar[0][0]
        bar[0][1] = rect[i]
    # bresenham(wind.scene, bar[0][0], bar[1][0], bar[0][1], bar[1][1], wind.pen_res)
    wind.scene.addLine(bar[0][0], bar[0][1], bar[1][0], bar[1][1], wind.pen_res)



def main():
    global wind
    app = QtWidgets.QApplication(sys.argv)
    wind = Visual()
    wind.show()
    app.exec_()


if __name__ == "__main__":
    main()