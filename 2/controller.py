from typing import Optional
from PyQt5.QtCore import Qt

from model import Model


class Controller:

    def __init__(self):
        self.view = None
        self.model: Optional[Model] = None

    def set_model(self, model: Model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def toggle_sliders(self, state):
        new_state = state == Qt.Checked
        self.model.set('show_sliders', new_state)

    def show_base_figures(self, state):
        new_state = state == Qt.Checked
        self.model.set('show_base_figures', new_state)

    def change_trans_x(self, value):
        self.model.set('trans_x', value)

    def change_trans_y(self, value):
        self.model.set('trans_y', value)

    def change_trans_x_slider(self, value):
        self.model.set('trans_x', value / 100)

    def change_trans_y_slider(self, value):
        self.model.set('trans_y', value / 100)

    def change_rotate(self, value):
        self.model.set('rotate', value)

    def change_scale_slider(self, value):
        relative = value / 100 * 4.9 + 0.1
        self.model.set('scale', relative)

    def change_scale(self, value):
        self.model.set('scale', value)
