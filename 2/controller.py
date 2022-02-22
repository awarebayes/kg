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

    def history_forward(self, callback):
        self.model.history_forward()
        callback()


    def change_float_var(self, value, field):
        self.model.set(field, value)

    def get_parameters(self):
        return self.model.get_parameters()

    def get_transformations(self):
        return self.model.get_transformations()

    def get_transform_array(self):
        return self.model.get('transform_array')

    def apply_transforms(self, dim):
        old_array = self.model.get('transform_array')
        new_array = copy.copy(old_array)
        new_transforms = self.model.get_transformations()
        new_array.append(new_transforms)
        self.model.set('transform_array', new_array)
        self.model.history_log('transform_array', old_array, new_array)

