from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from model import Model
from functools import partial


class View(Ui_MainWindow):
    def __init__(self, controller):
        self.controller = controller
        super().__init__()

        self.fields_to_model = {
            "TransX": "trans_x",
            "TransY": "trans_y",
            "Scale": "scale",
            "Rotate": "rotate",
            "A": "a",
            "B": "b",
            "C": "c",
            "D": "d",
            "R": "r",
        }

        self.model_to_fields = {
            v: k for k, v in self.fields_to_model.items()
        }

    def register_controller_callbacks(self):
        for self_field, model_field in self.fields_to_model.items():
            sb = getattr(self, f"{self_field}SB")
            sb_callback = partial(self.controller.change_float_var, field=model_field)
            sb.valueChanged.connect(sb_callback)

    def register_view_callbacks(self, model):
        for field in self.model_to_fields.keys():
            model.add_callback(field, lambda *args: self.frame.update())

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
