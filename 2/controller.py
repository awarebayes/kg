import copy
from typing import Optional
from PyQt5.QtCore import Qt

from model import Model, ModelWithHistory
from transforms import apply_transform


class Controller:
    def __init__(self):
        self.view = None
        self.model: Optional[ModelWithHistory] = None

    def set_model(self, model: ModelWithHistory):
        self.model = model

    def set_view(self, view):
        self.view = view

    def toggle_sliders(self, state):
        new_state = state == Qt.Checked
        self.model.set("show_sliders", new_state)

    def show_base_figures(self, state):
        new_state = state == Qt.Checked
        self.model.set("show_base_figures", new_state)

    def history_backward(self, callback):
        self.model.history_back()
        callback()
        state = self.model.get_state()
        self.view.update_sliders(state)

    def history_forward(self, callback):
        self.model.history_forward()
        callback()
        state = self.model.get_state()
        self.view.update_sliders(state)

    def change_float_var(self, value, field):
        self.model.set(field, value)

    def get_parameters(self):
        return self.model.get_parameters()

    def get_transform_array(self):
        return self.model.get("transform_array")

    def register_transform(self, kind: str):
        self.model.register_transformation(kind)

    def get_sr_point(self):
        return self.model.get("sr_center_x"), self.model.get("sr_center_y")

    def mute_model(self):
        self.model.muted = True

    def unmute_model(self):
        self.model.muted = False
