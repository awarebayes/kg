import tkinter as tk
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
    label: str


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


class PointView(tk.Frame):
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
        self.label_dropdown = tk.OptionMenu(self.misc_frame, self.label_var, "Set 1", "Set 2")
        self.delete_button = tk.Button(self.misc_frame, text="x", command=self.destroy)

        self.x_frame.grid(row=0, column=0)
        self.y_frame.grid(row=0, column=1)
        self.misc_frame.grid(row=0, column=2)

        self.x_label.grid(row=0, column=0)
        self.x_input.grid(row=0, column=1)

        self.y_label.grid(row=0, column=0)
        self.y_input.grid(row=0, column=1)

        self.label_dropdown.grid(row=0, column=0)
        self.delete_button.grid(row=0, column=1)
        self.is_destroyed = False

    def destroy(self) -> None:
        self.is_destroyed = True
        super().destroy()

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


class SidePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_button = tk.Button(self, text="add 1", command=self.add_point)
        self.add_button.grid(row=0, column=0)

        self.scrollable_frame = ScrolledFrame(self)
        self.point_components = []

        self.scrollable_frame.grid(row=1, column=0)
        self.point_count = 0

    def add_point(self):
        component = PointView(self.scrollable_frame)
        component.grid(column=0, row=self.point_count)
        self.point_count += 1
        self.point_components.append(component)


class Canvas(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(Canvas, self).__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg="black", height=800, width=800)
        self.canvas.pack()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.side_panel = SidePanel(self)
        self.canvas = Canvas(self)
        self.side_panel.pack(side=tk.LEFT, expand=True, fill="both")
        self.canvas.pack(side=tk.LEFT)


if __name__ == "__main__":
    app = App()
    app.mainloop()
