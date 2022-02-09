import tkinter as tk
from dataclasses import dataclass
from tkinter import scrolledtext, messagebox
from prettytable import PrettyTable
from point_widgets import ShowPointEditor, AskPointIndex
from functools import wraps


@dataclass
class Point:
    x: float
    y: float


def close_other_windows(method):
    @wraps(method)
    def inner(self, *method_args, **method_kwargs):
        for w in self.opened_windows:
            w.destroy()
            w.update()
        w = method(self, *method_args, **method_kwargs)
        self.opened_windows = [w]
    return inner


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

        self.add_button = tk.Button(self, text="Add point", command=self.dialog_add_point)
        self.calculate_button = tk.Button(self, text="Calculate", command=self.dialog_add_point)

        self.edit_button = tk.Button(self, text="Edit point", command=self.dialog_edit_point)
        self.delete_button = tk.Button(self, text="Delete point", command=self.dialog_delete_point)
        self.clear_button = tk.Button(self, text="Delete all points", command=self.call_delete_all_points)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45,
                                              height=50, font=("Times New Roman", 14))
        self.text_area.config(state=tk.DISABLED)

        self.add_button.grid(row=0, column=0)
        self.calculate_button.grid(row=0, column=1)
        self.edit_button.grid(row=1, column=0)
        self.delete_button.grid(row=1, column=1)
        self.clear_button.grid(row=1, column=2)
        self.text_area.grid(row=2, column=0, columnspan=3)
        self.get_points = get_points
        self.set_points = set_points
        self.reformat_table()
        self.opened_windows = []

    @close_other_windows
    def dialog_add_point(self):
        return ShowPointEditor(self.add_point)

    @close_other_windows
    def dialog_delete_point(self):
        max_index = len(self.get_points()) - 1
        return AskPointIndex(max_index, self.remove_point)

    @close_other_windows
    def dialog_edit_point(self):

        def show_editor(index):
            initial_point = self.fetch_point(index)
            return ShowPointEditor(lambda p: self.edit_point(index, p), initial_point)

        max_index = len(self.get_points()) - 1
        return AskPointIndex(max_index, show_editor)

    def add_point(self, point):
        points = self.get_points()
        if point in points:
            messagebox.showwarning("Warning", "Point is already in the set, ignoring")
        else:
            points.append(point)
            self.set_points(points)

    def call_delete_all_points(self):
        self.set_points([])

    def remove_point(self, index):
        points = self.get_points()
        points.pop(index)
        self.set_points(points)

    def fetch_point(self, index):
        return self.get_points()[index]

    def edit_point(self, index, point):
        points = self.get_points()
        points[index] = point
        self.set_points(points)

    def reformat_table(self):
        if not self.get_points():
            string = "No points no show yet, click `add_point`"
        else:
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
        self.points = Observable(list())
        self.side_panel = SidePanel(self, self.points.get, self.points.set)
        self.canvas = Canvas(self)
        self.side_panel.pack(side=tk.LEFT, expand=True, fill="both")
        self.canvas.pack(side=tk.LEFT)

        self.points.add_callback(self.side_panel.reformat_table)

    def get_points(self):
        return self.points


if __name__ == "__main__":
    app = App()
    app.mainloop()
