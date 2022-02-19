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
            "ScaleX": "scale_x",
            "ScaleY": "scale_y",
            "Rotate": "rotate",
            "SRCenterX": "sr_center_x",
            "SRCenterY": "sr_center_y",
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

        self.pushButton.clicked.connect(self.controller.history_backward)
        self.pushButton_2.clicked.connect(self.controller.history_forward)

    def toggle_can_go_forward(self, can_go):
        if can_go:
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setDisabled(True)

    def register_view_callbacks(self, model):
        for field in self.model_to_fields.keys():
            model.add_callback(field, lambda *args: self.frame.update())
        model.add_callback('can_go_forward', self.toggle_can_go_forward)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
