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
        self.model.set("show_sliders", new_state)

    def show_base_figures(self, state):
        new_state = state == Qt.Checked
        self.model.set("show_base_figures", new_state)

    def change_float_var(self, value, field):
        self.model.set(field, value)

    def get_parameters(self):
        return self.model.get_parameters()

    def get_transformations(self):
        return self.model.get_transformations()
