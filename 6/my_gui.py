from collections import defaultdict
import time
from math import sin, cos, radians, sqrt
from typing import Tuple, List, Callable, Optional, DefaultDict

from matplotlib import pyplot as plt

from design import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem
from dataclasses import dataclass
from my_types import TwoPointEdge, PixelColor, two_point_edge_to_edge, Drawer, Point
from algorithms import method_with_seed
from sys import exit
from ellipse import method_middle_point_ellipse

EPS = 10


@dataclass
class Model:
    edges: List[TwoPointEdge]
    point_count: int
    seed: Point = (400, 400)
    draw_ellipse: bool = False

    def reset(self):
        self.edges = []
        self.seed = (400, 400)
        self.point_count = 0
        self.draw_ellipse = False


color_map = {
    "Белый": Qt.white,
    "Черный": Qt.black,
    "Зеленый": Qt.green,
    "Красный": Qt.red,
    "Синий": Qt.blue,
}


def hex_area(r):
    return 6 * r**2 * sqrt(3) / 4


def hexagon(init_theta, radius) -> List[TwoPointEdge]:
    theta = init_theta
    points: List[Point] = []

    theta_rad = radians(theta)
    point = int(sin(theta_rad) * radius), int(cos(theta_rad) * radius)
    points.append(point)
    while theta < 360 + init_theta:
        theta_rad = radians(theta)
        point = int(sin(theta_rad) * radius), int(cos(theta_rad) * radius)
        points.append(point)
        theta += 60

    edges = []
    for p1, p2 in zip(points, points[1:] + [points[0]]):
        edges.append((p1, p2))
    return edges


def dummy_drawer(canvas_width, canvas_height):
    def dummy_place(x1, y1, x2, y2):
        pass

    return Drawer(
        dummy_place,
        dummy_place,
        dummy_place,
        dummy_place,
        defaultdict(lambda: PixelColor.BACKGROUND),
        canvas_x_low=-canvas_width / 2,
        canvas_x_high=+canvas_width / 2,
        canvas_y_low=-canvas_height / 2,
        canvas_y_high=+canvas_height / 2,
    )


class GuiMainWin(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model(edges=[], point_count=0)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.black)
        self.graphicsView.setScene(self.scene)
        graphics_dim = self.graphicsView.size()
        self.scene.setSceneRect(0, 0, graphics_dim.width()-2, graphics_dim.height()-2)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Индекс", "X", "Y"])
        self.tableWidget.setRowCount(100)
        self.connect()
        self.change_bg_color()
        self.set_seed(graphics_dim.width()//2, graphics_dim.height()//2)

    def add_point(self, x, y):
        index = self.model.point_count
        self.model.point_count += 1

        print("added at index", index, x, y)

        self.tableWidget.setItem(index, 0, QTableWidgetItem(str(index)))
        self.tableWidget.setItem(index, 1, QTableWidgetItem(str(x)))
        self.tableWidget.setItem(index, 2, QTableWidgetItem(str(y)))
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

    def connect(self):
        self.bg_color.currentIndexChanged.connect(self.change_bg_color)
        self.exit_btn.clicked.connect(lambda *args: exit(0))
        self.time_btn.clicked.connect(self.time_benchmark)
        self.draw_circ_btn.clicked.connect(lambda: self.add_ellipse(None))

    def clear(self):
        self.tableWidget.clear()
        self.scene.clear()
        self.tableWidget.setHorizontalHeaderLabels(["Индекс", "X", "Y"])
        self.model.reset()

    def change_bg_color(self):
        color = color_map[self.bg_color.currentText()]
        self.scene.setBackgroundBrush(color)

    def get_draw_edge(self):
        color = color_map[self.border_color.currentText()]

        def draw_edge(x1, y1, x2, y2):
            self.scene.addLine(x1, y1, x2, y2, color)

        return draw_edge

    def get_draw_inside(self):
        color = color_map[self.fill_color.currentText()]

        def draw_inside(x1, y1, x2, y2):
            self.scene.addLine(x1, y1, x2, y2, color)

        return draw_inside

    def get_draw_bg(self):
        color = color_map[self.bg_color.currentText()]

        def draw_bg(x1, y1, x2, y2):
            self.scene.addLine(x1, y1, x2, y2, color)

        return draw_bg

    def get_draw_edge_log(self):
        color = color_map[self.border_color.currentText()]

        def draw_edge(x1, y1, x2, y2):
            self.scene.addLine(x1, y1, x2, y2, color)
            self.model.edges.append(((x1, y1), (x2, y2)))

        return draw_edge

    def get_drawer(self):
        return Drawer(
            _line_edge=self.get_draw_edge(),
            _line_inside=self.get_draw_inside(),
            _line_mark=self.get_draw_inside(),
            _line_bg=self.get_draw_bg(),
            buffer=defaultdict(lambda: PixelColor.BACKGROUND),
            canvas_x_low=0,
            canvas_x_high=self.graphicsView.size().width(),
            canvas_y_low=0,
            canvas_y_high=self.graphicsView.size().height(),
        )

    def fill(self):
        self.scene.clear()
        drawer = self.get_drawer()

        if self.model.draw_ellipse:
            self.add_ellipse(drawer)

        edges = self.model.edges
        edges = list(map(two_point_edge_to_edge, edges))

        delay = 0
        if self.delay_checkbox.isChecked():
            delay = self.delay_inp.value()
        method_with_seed(edges, drawer, self.model.seed, delay)

    def transform(self, x, y):
        x -= self.graphicsView.pos().x()

        y -= self.graphicsView.pos().y()

        return x, y

    def get_ver_hor_line(self, x, y, last_point):
        if abs(x - last_point[0]) < abs(y - last_point[1]):
            x = last_point[0]
        else:
            y = last_point[1]
        return x, y

    def time_benchmark(self, warmup=False, trials=1):

        if not warmup:
            self.time_benchmark(warmup=True, trials=5)

        radius = list(range(5, 100, 5))
        area = list(map(hex_area, radius))
        time_elapsed = []
        for r in radius:
            total = 0
            for t in range(trials):
                fig = hexagon(5, r)
                edges = list(map(two_point_edge_to_edge, fig))
                time_start = time.time()
                method_with_seed(edges,
                                 dummy_drawer(500, 500),
                                 (0, 0),
                                 0)
                total += time.time() - time_start
            time_elapsed.append(total / trials)

        if warmup:
            return

        plt.figure(figsize=(10, 6))
        plt.xlabel("Площадь шестиугольника (количество пикселей)")
        plt.ylabel("Время (в миллисекундах)")
        plt.title("Зависимость времени работы от площади", size=9)

        plt.plot(area, time_elapsed, linewidth=1, linestyle="-", color="blue")
        plt.show()

    def set_seed(self, x, y):
        bg_color = color_map[self.bg_color.currentText()]
        self.scene.addEllipse(*self.model.seed, 1, 1, pen=bg_color)
        self.model.seed = (x, y)
        self.scene.addEllipse(*self.model.seed, 1, 1, pen=Qt.darkCyan)
        self.zatr_pos_label.setText(f"Затравка: {x}, {y}")

    def add_ellipse(self, drawer=None):
        self.model.draw_ellipse = True
        dim = self.graphicsView.size()
        ellipse = (dim.width()//2, dim.height()//2, 300, 200)
        if drawer is None:
            drawer = self.get_drawer()
        method_middle_point_ellipse(*ellipse, drawer.pixel_edge)
