import numpy as np

from ui.gui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPen

from math import *
from graphics import *
import sys

EPS = 10

color_map = {
    "Красный": Qt.red,
    "Черный": Qt.black,
    "Белый": Qt.white,
    "Синий": Qt.blue,
    "Зеленый": Qt.green,
    "Желтый": Qt.yellow,
}


class GuiMainWin(Ui_MainWindow):
    bg_color = Qt.black
    cutter_color = QtGui.QColor("#FF0000")
    fig_color = QtGui.QColor("#0C69FF")
    task_color = QtGui.QColor("#00FF00")

    pen_cutter = QPen(cutter_color)
    pen_fig = QPen(fig_color)
    pen_task = QPen(task_color)

    is_cutter, is_fig = True, False
    is_locked_cutter, is_locked_fig = False, False
    first_point, last_point = None, None

    def __init__(self):
        self.point_on_otsek_flag = False

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)

        self.size_x = self.graphicsView.size().width()
        self.size_y = self.graphicsView.size().height()

        self.graphicsView.setSceneRect(0, 0, self.size_x - 4, self.size_y - 4)
        self.graphicsView.setScene(self.scene)

        self.ChangeColorCutter.currentTextChanged.connect(self.change_color_cutter)
        self.ChangeColorFig.currentTextChanged.connect(self.change_color_fig)
        self.ChangeColorTask.currentTextChanged.connect(self.change_color_task)

        self.change_color_cutter()
        self.change_color_fig()
        self.change_color_task()

        self.input_status.setText("Сейчас вводится: отсекатель")

        self.LockLine.clicked.connect(self.lock_fig)

        self.DoTask.clicked.connect(self.clipping_fig)
        self.Clean.clicked.connect(self.clean_screen)
        self.ExitButton.clicked.connect(lambda: sys.exit(0))
        self.PointOnOtsek.clicked.connect(self.point_on_oksekatel)
        self.enter_button.clicked.connect(self.add_point_from_input)

        self.cutter_arr = []
        self.fig_arr = []
        self.result = []
        # self.edges_cutter = []
        self.clean_screen()

    def change_color_cutter(self):
        color = color_map[self.ChangeColorCutter.currentText()]
        self.set_color_cutter(color)

    def set_color_cutter(self, color):
        self.cutter_color = color
        self.pen_cutter = QPen(color)

    def change_color_fig(self):
        color = color_map[self.ChangeColorFig.currentText()]
        self.set_color_fig(color)

    def set_color_fig(self, color):
        self.fig_color = color
        self.pen_fig = QPen(color)

    def change_color_task(self):
        color = color_map[self.ChangeColorTask.currentText()]
        self.set_color_task(color)

    def set_color_task(self, color):
        self.task_color = color
        self.pen_task = QPen(color)

    def transform(self, x, y):
        x -= self.graphicsView.pos().x()
        if not (0 <= x <= self.graphicsView.size().width()):
            return None

        y -= self.graphicsView.pos().y()
        if not (0 <= y <= self.graphicsView.size().height()):
            return None
        y = -y + self.graphicsView.size().height()

        return x, y

    def add_point_from_input(self):
        x = self.point_x_entry.value()
        y = self.point_y_entry.value()
        self.draw_line(x, y, False)

    def draw_line(self, x, y, flag):
        if self.is_locked_fig:
            return

        if self.point_on_otsek_flag:
            x, y = self.project_to_otsek_as_closest(x, y)
            self.point_on_otsek_flag = False

        if self.first_point == None:
            self.first_point = (x, y)
            self.last_point = (x, y)
            if self.is_cutter:
                self.cutter_arr.append(Point(x, y))
            else:
                self.fig_arr.append(Point(x, y))
        else:
            if (
                abs(x - self.first_point[0]) < EPS
                and abs(y - self.first_point[1]) < EPS
            ):
                x, y = self.first_point[0], self.first_point[1]
                if self.is_cutter:
                    self.is_locked_cutter = True
                else:
                    self.is_locked_fig = True

            if flag:
                if abs(x - self.last_point[0]) < abs(y - self.last_point[1]):
                    x = self.last_point[0]
                else:
                    y = self.last_point[1]

            points = [self.last_point[0],
                      -self.last_point[1] + self.size_y,
                      x,
                      -y + self.size_y]


            if self.is_cutter:
                self.scene.addLine(
                    *points,
                    self.pen_cutter,
                )

                self.cutter_arr.append(Point(x, y))
                points[-1] = y
                self.add_table_points(self.OtsekTable, [*self.last_point, x, y])

                if self.is_locked_cutter:
                    self.is_cutter = False
                    self.is_fig = True
            else:
                self.fig_arr.append(Point(x, y))
                self.scene.addLine(
                    *points,
                    self.pen_fig,
                )
                points[-1] = y
                self.add_table_points(self.FigTable, [*self.last_point, x, y])


            self.last_point = (x, y)
            if self.is_locked_cutter:
                self.first_point, self.last_point = None, None
                self.is_locked_cutter = False

    def add_table_points(self, table, points):
        for i in range(len(points)):
            table.setItem(table.count, i, QTableWidgetItem(str(points[i])))
        table.count += 1

    def lock_fig(self):
        x, y = self.first_point[0], self.first_point[1]
        points = [self.last_point[0],
                  -self.last_point[1] + self.graphicsView.size().height(),
                  x,
                  -y + self.graphicsView.size().height(), ]
        if self.is_cutter:
            self.scene.addLine(
                *points,
                self.pen_cutter,
            )

            self.add_table_points(self.OtsekTable, [*self.last_point, x, y])
            self.cutter_arr.append(self.cutter_arr[0])
            self.is_cutter = False
            self.first_point, self.last_point = None, None
            self.input_status.setText("Сейчас вводится: фигура")
        else:
            self.scene.addLine(
                *points,
                self.pen_fig,
            )

            self.add_table_points(self.FigTable, [*self.last_point, x, y])
            self.is_locked_fig = True
            self.input_status.setText("Сейчас вводится: ничего")

    def point_on_oksekatel(self):
        if not self.cutter_arr:
            return QMessageBox.warning(None, "", "Введите отсекатель!!!")
        self.point_on_otsek_flag = True

    def project_to_otsek_as_closest(self, x, y):
        def project(line, point):
            x = np.array(point)
            u = np.array([line[0].x, line[0].y], dtype=np.float32)
            v = np.array([line[1].x, line[1].y], dtype=np.float32)
            n = v - u
            n /= np.linalg.norm(n, 2)
            P = u + n * np.dot(x - u, n)
            return P.astype(np.long)

        cutter = self.cutter_arr
        point = np.array((x, y))
        projections = []
        l2s = []
        for line in zip(cutter, cutter[1:]):
            projection = project(line, point)
            l2 = np.linalg.norm(projection - point)
            projections.append(projection)
            l2s.append(l2)
        min_l2 = np.argmin(l2s)
        return projections[min_l2]


    def clean_screen(self):
        self.scene.clear()
        self.first_point, self.last_point = None, None
        self.is_cutter, self.is_fig = True, False
        self.is_locked_cutter, self.is_locked_fig = False, False
        self.cutter_arr = []
        self.fig_arr = []
        self.result = []
        for t in [self.FigTable, self.OtsekTable]:
            t.clear()
            t.setColumnCount(4)
            t.setRowCount(100)
            t.setHorizontalHeaderLabels(["x1", "y1", "x2", "y2"])
            t.count = 0
        self.input_status.setText("Сейчас вводится: отсекатель")

    def draw_result(self):
        for i in range(len(self.fig_arr)):
            self.scene.addLine(
                self.fig_arr[i].x,
                -self.fig_arr[i].y + self.size_y,
                self.fig_arr[(i + 1) % (len(self.fig_arr))].x,
                -self.fig_arr[(i + 1) % len(self.fig_arr)].y + self.size_y,
                self.pen_task,
            )


    def clipping_fig(self):
        dir = is_convex_polygon(self.cutter_arr)
        if not dir:
            return QMessageBox.warning(None, "Warning!", "Отсекатель не выпуклый")
        if not self.fig_arr:
            return QMessageBox.warning(None, "Warning!", "Фигура не введена")

        for i in range(len(self.cutter_arr) - 1):
            self.result = []
            for j in range(len(self.fig_arr)):
                if not j:
                    first = self.fig_arr[j]
                else:
                    point = find_cross(
                        last,
                        self.fig_arr[j],
                        self.cutter_arr[i],
                        self.cutter_arr[i + 1],
                    )
                    if point != None:
                        self.result.append(point)

                last = self.fig_arr[j]
                if (
                    is_visible_point(last, self.cutter_arr[i], self.cutter_arr[i + 1])
                    * dir
                    >= 0
                ):
                    self.result.append(last)

            if len(self.result):
                point = find_cross(
                    last, first, self.cutter_arr[i], self.cutter_arr[i + 1]
                )
                if point != None:
                    self.result.append(point)
            if not len(self.result):
                return
            self.fig_arr = self.result

        self.draw_result()


def is_convex_polygon(arr):
    edges = make_edges(arr)
    is_neg, is_pos, is_zero = False, False, False
    vect_mul = None

    for i in range(len(edges)):
        vect_mul = vector_mul(edges[(i + 1) % len(edges)], edges[i])

        if vect_mul < 0:
            is_neg = True
        elif vect_mul > 0:
            is_pos = True
        else:
            is_zero = True

    if ((is_neg and not is_pos) or (is_pos and not is_neg)) and not is_zero:
        return copysign(1, vect_mul)
    else:
        return False


def make_edges(arr):
    edges = []
    for i in range(len(arr) - 1):
        add_edge(edges, arr[i], arr[i + 1])
    for i in range(len(edges)):
        print(edges[i].x1, edges[i].y1, edges[i].x2, edges[i].y2)

    return edges


def vector_mul(vector1, vector2):
    return vector1.x * vector2.y - vector2.x * vector1.y


def line_charact(point_1, point_2):
    A = point_2.y - point_1.y
    B = point_1.x - point_2.x
    C = point_2.x * point_1.y - point_1.x * point_2.y

    return A, B, C


def matrix_det(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def is_visible_point(point, cut_edge_1, cut_edge_2):
    return (point.x - cut_edge_1.x) * (cut_edge_2.y - cut_edge_1.y) - (
        point.y - cut_edge_1.y
    ) * (cut_edge_2.x - cut_edge_1.x)


def find_cross(edge_start, edge_end, cut_start, cut_end):
    if is_cross(edge_start, edge_end, cut_start, cut_end):
        return point_cross(edge_start, edge_end, cut_start, cut_end)
    return None


def is_cross(edge_start, edge_end, cut_start, cut_end):
    flag_1 = is_visible_point(edge_start, cut_start, cut_end)
    flag_2 = is_visible_point(edge_end, cut_start, cut_end)

    if flag_1 <= 0 and flag_2 >= 0 or flag_1 >= 0 and flag_2 <= 0:
        return True
    else:
        return False


def point_cross(edge_start, edge_end, cut_start, cut_end):
    A1, B1, C1 = line_charact(edge_start, edge_end)
    A2, B2, C2 = line_charact(cut_start, cut_end)

    det = matrix_det(A1, B1, A2, B2)
    if not det:
        return edge_end
    else:
        det_x = matrix_det(-C1, B1, -C2, B2)
        det_y = matrix_det(A1, -C1, A2, -C2)

        point = Point(det_x / det, det_y / det)

        return point
