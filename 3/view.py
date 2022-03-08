import math
from dataclasses import dataclass
import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPen
from PyQt5.QtWidgets import QWidget, QColorDialog, QGraphicsScene, QMessageBox
from matplotlib import pyplot as plt

from algorithms import draw_line

from ui import Ui_MainWindow
from step_counter import StepCounter, WuStepCounter


@dataclass
class State:
    bg_color: tuple = (255, 255, 255)
    line_color: tuple = (0, 0, 0)


def change_bg_color(widget: QWidget, color):
    palette = QPalette()
    color = QColor(*color)
    palette.setColor(QPalette.Window, color)
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)
    widget.show()


class View(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.scene = None
        self.state = State()

    def on_setup_complete(self):
        self.update_color_preview()
        self.connect()
        self.set_scene()

    def set_scene(self):
        self.scene = QGraphicsScene()
        height = self.graphicsView.height()
        width = self.graphicsView.width()
        self.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(0, 0, width - 2, height - 2)

    def connect(self):
        self.change_bg_color_button.clicked.connect(self.on_change_bg_button_clicked)
        self.change_line_color_button.clicked.connect(self.on_change_line_button_clicked)
        self.plot_line_button.clicked.connect(self.on_draw_line_button_clicked)
        self.clear_buton.clicked.connect(self.on_clear_button_clicked)
        self.plot_sun_button.clicked.connect(self.on_plot_sun_button_clicked)
        self.time_comparison_button.clicked.connect(self.on_time_comparison_button_clicked)
        self.step_comparison_button.clicked.connect(self.on_step_comparison_button_clicked)
        self.all_step_comparison_button.clicked.connect(self.on_compare_all_button_clicked)
        self.action.triggered.connect(lambda: exit(0))

    def update_color_preview(self):
        change_bg_color(self.bg_color_preview, self.state.bg_color)
        change_bg_color(self.line_color_preview, self.state.line_color)

    def on_change_bg_button_clicked(self):
        color = QColorDialog.getColor(Qt.white, None)
        val = color.getRgb()
        val = val[0], val[1], val[2]
        self.state.bg_color = val
        self.update_color_preview()
        css = "background-color: #{0:02x}{1:02x}{2:02x}".format(*val)
        self.graphicsView.setStyleSheet(css)

    def on_change_line_button_clicked(self):
        color = QColorDialog.getColor(Qt.black, None)
        val = color.getRgb()
        val = val[0], val[1], val[2]
        self.state.line_color = val
        self.update_color_preview()

    def on_clear_button_clicked(self):
        self.scene.clear()

    def get_place_pixel(self):
        color = self.state.line_color
        color = QColor.fromRgb(*color)

        def place_pixel(x, y, intensity=255):
            QColor.setAlpha(color, intensity)
            pen = QPen(color)
            self.scene.addLine(x, y, x, y, pen)

        return place_pixel

    def draw_line_with_library(self, start, end):
        color = self.state.line_color
        pen = QPen(QColor.fromRgb(*color))
        self.scene.addLine(*start, *end, pen)

    def on_draw_line_button_clicked(self):
        algorithm = self.algorithm_selection.currentText()
        place_pixel = self.get_place_pixel()

        start = self.line_start_x.value(), self.line_start_y.value()
        end = self.line_end_x.value(), self.line_end_y.value()

        if start == end:
            QMessageBox.information(None, "Info", "Отрисована только единственная точка")
            place_pixel(*start)
            return

        if algorithm != "Из Библиотеки":
            draw_line(algorithm, start, end, place_pixel)
        else:
            self.draw_line_with_library(start, end)

    def on_plot_sun_button_clicked(self):
        algorithm = self.algorithm_selection.currentText()
        place_pixel = self.get_place_pixel()

        if algorithm != "Из Библиотеки":
            draw_line_overload = lambda start_, end_: draw_line(algorithm, start_, end_, place_pixel)
        else:
            draw_line_overload = self.draw_line_with_library

        start = (self.graphicsView.width() // 2, self.graphicsView.height() // 2)

        d_theta = self.sun_step_deg.value()
        rad = self.sun_radius.value()

        theta = 0
        while theta < 360:
            radians = math.radians(theta)

            r_vector = math.cos(radians) * rad, math.sin(radians) * rad
            r_vector = int(r_vector[0]), int(r_vector[1])
            end = start[0] + r_vector[0], start[1] + r_vector[1]
            draw_line_overload(start, end)
            print("drawn", theta)

            theta += d_theta

    def on_time_comparison_button_clicked(self):
        algos = ["ЦДА", "Брезенхем",  "Брезенхем Целочисленный", 'Брезенхем Сглаживание', "Ву"]

        time_comp = {algo: [] for algo in algos}
        rad = 300

        def dummy(x, y, intensity=0):
            pass

        for algo in algos:
            theta = 0
            while theta <= 90:
                radians = math.radians(theta)
                r_vector = math.cos(radians) * rad, math.sin(radians) * rad
                r_vector = int(r_vector[0]), int(r_vector[1])

                start = time.time_ns()
                draw_line(algo, (0, 0), r_vector, dummy)
                end = time.time_ns()

                elapsed = end - start
                theta += 1
                time_comp[algo].append(elapsed)

        fig = plt.figure(figsize=(15, 10))
        plt.bar(time_comp.keys(), [np.mean(v) for v in time_comp.values()])
        plt.xlabel(f"Алгоритм")
        plt.ylabel(f"Время (наносекунды)")
        plt.title(f"Время выполнения, отрисовка не учитывается, усреднено по градусу от [0..90]")
        plt.show()


    def on_compare_all_button_clicked(self):
        d_theta = 1
        thetas = range(0, 91)

        algos = ["ЦДА", "Брезенхем",  "Брезенхем Целочисленный", 'Брезенхем Сглаживание', "Ву"]
        steps = {algo: [] for algo in algos}

        time_comp = {algo: [] for algo in algos}
        rad = 300

        def dummy(x, y, intensity=0):
            pass

        for algo in algos:
            theta = 0
            while theta <= 90:
                radians = math.radians(theta)
                r_vector = math.cos(radians) * rad, math.sin(radians) * rad
                r_vector = int(r_vector[0]), int(r_vector[1])
                counter = StepCounter() if algo != "Ву" else WuStepCounter()
                draw_line(algo, (0, 0), r_vector, counter.count_step)
                steps[algo].append(counter.steps)
                theta += d_theta

        for algo in algos:
            plt.plot(thetas, steps[algo], label=algo)
        plt.xlabel(f"Угол в градусах (шаг={d_theta})")
        plt.ylabel(f"Кол-во шагов (радиус={rad})")
        plt.title(f"Кол-во шагов для алгоритмов")
        plt.legend()
        plt.grid()
        plt.xticks(np.arange(0, 90, 5))
        plt.show()

    def on_step_comparison_button_clicked(self):
        algorithm = self.algorithm_selection.currentText()

        if algorithm == "Из Библиотеки":
            QMessageBox.critical(None, "Critical", "Нельзя измерить кол-во шагов для алгоритма из библиотеки")
            return

        d_theta = 1
        rad = 300
        steps = []
        thetas = []

        theta = 0
        while theta <= 90:
            radians = math.radians(theta)

            r_vector = math.cos(radians) * rad, math.sin(radians) * rad
            r_vector = int(r_vector[0]), int(r_vector[1])
            counter = StepCounter() if algorithm != "Ву" else WuStepCounter()
            draw_line(algorithm, (0, 0), r_vector, counter.count_step)

            steps.append(counter.steps)
            thetas.append(theta)
            theta += d_theta

        plt.plot(thetas, steps)
        plt.xlabel(f"Угол в градусах (шаг={d_theta})")
        plt.ylabel(f"Кол-во шагов (радиус={rad})")
        plt.title(f"Кол-во шагов для алгоритма {algorithm}")
        plt.grid()
        plt.xticks(np.arange(0, 90, 5))
        plt.show()
