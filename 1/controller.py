from point_widgets import ShowPointEditor, AskPointIndex
from functools import wraps
from tkinter import messagebox


def close_other_windows(method):
    @wraps(method)
    def inner(self, *method_args, **method_kwargs):
        for w in self.opened_windows:
            w.destroy()
            w.update()
        w = method(self, *method_args, **method_kwargs)
        self.opened_windows = [w]
    return inner


class Controller:
    def __init__(self, model):
        self.opened_windows = []
        self.model = model

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

    def delete_all_points(self):
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

    def get_points(self):
        return self.model.get('points')

    def set_points(self, value):
        self.model.set('points', value)