import tkinter as tk


class PointView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.x_var.set("0.0")
        self.y_var.set("0.0")
        self.label_var = tk.StringVar()
        self.label_var.set("Set 1")

        self.x_frame = tk.Frame(self)
        self.x_label = tk.Label(self.x_frame, text="x:")
        self.x_input = tk.Entry(self.x_frame, textvariable=self.x_var, width=16)

        self.y_frame = tk.Frame(self)
        self.y_label = tk.Label(self.y_frame, text="y:")
        self.y_input = tk.Entry(self.y_frame, textvariable=self.y_var, width=16)

        self.misc_frame = tk.Frame(self)
        self.add_button = tk.Button(self.misc_frame, text="Add point", command=self.destroy)

        self.x_frame.grid(row=0, column=0)
        self.y_frame.grid(row=0, column=1)
        self.misc_frame.grid(row=0, column=2)

        self.x_label.grid(row=0, column=0)
        self.x_input.grid(row=0, column=1)

        self.y_label.grid(row=0, column=0)
        self.y_input.grid(row=0, column=1)

        self.add_button.grid(row=0, column=1)

    def get_point(self):
        x_var = self.x_var.get()
        y_var = self.y_var.get()
        try:
            x = float(x_var)
            y = float(y_var)
            label = self.label_var.get()
            return Point(x, y, label)
        except ValueError:
            error_message = "Ошибка: точка указана неверно"
            if not is_float(x_var):
                error_message += f"\n X-компонента точки указана неверно: {x_var}"
            if not is_float(y_var):
                error_message += f"\n Y-компонента точки указана неверно: {y_var}"
            if self.label_var.get() not in ["Set 1", "Set 2"]:
                error_message += "\n Label точки указан неверно. Не знаю, как у вас это получилось"
            raise ValueError(error_message)
