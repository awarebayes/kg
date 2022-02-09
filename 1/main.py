import tkinter as tk
import tkinter.font as tkFont
from dataclasses import dataclass
from tkinter import scrolledtext
from prettytable import PrettyTable

@dataclass
class Point:
    x: float
    y: float


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


class Observable:
    def __init__(self, value):
        self._value = value
        self._callbacks = []

    def notify(self):
        for cb in self._callbacks:
            cb()

    def set(self, value):
        self._value = value
        self.notify()

    def get(self):
        return self._value

    def add_callback(self, cb):
        self._callbacks.append(cb)


class SidePanel(tk.Frame):
    def __init__(self, parent, get_points, set_points):
        super().__init__(parent)

        self.add_button = tk.Button(self, text="Add point", command=self.add_point)
        self.edit_button = tk.Button(self, text="Edit point", command=self.add_point)
        self.delete_button = tk.Button(self, text="Delete point", command=self.add_point)
        self.clear_button = tk.Button(self, text="Delete all points", command=self.add_point)
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45,
                                              height=50, font=("Times New Roman", 14))
        self.text_area.config(state=tk.DISABLED)

        self.add_button.grid(row=0, column=0, columnspan=3)
        self.edit_button.grid(row=1, column=0)
        self.delete_button.grid(row=1, column=1)
        self.clear_button.grid(row=1, column=2)
        self.text_area.grid(row=2, column=0, columnspan=3)
        self.get_points = get_points
        self.set_points = set_points

    def add_point(self):
        point =

    def reformat_table(self):
        table = PrettyTable()
        table.field_names = ["Idx", "X", "Y"]
        for i, point in enumerate(self.get_points()):
            table.add_row([i, point.x, point.y])
        string = table.get_string()

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, string)
        self.text_area.config(state=tk.DISABLED)

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

        self.points = Observable(list())
        self.points.add_callback(self.side_panel.reformat_table)


    def add_point(self, point: Point):
        self.points.append(point)

    def get_points(self):
        return self.points


if __name__ == "__main__":
    app = App()
    app.mainloop()
