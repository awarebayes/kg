from point_widgets import ShowPointEditor, AskPointIndex
from functools import wraps
from tkinter import messagebox
import solution


def close_other_windows(method):
    @wraps(method)
    def inner(self, *method_args, **method_kwargs):
        for w in self.opened_windows:
            w.destroy()
            w.update()
        w = method(self, *method_args, **method_kwargs)
        self.opened_windows = [w]

    return inner


def has_any_triangles(points):
    try:
        possible_triangles = solution.triangles_iterator(points)
        next(possible_triangles)
        return True
    except StopIteration:
        return False


class Controller:
    def __init__(self, model):
        self.opened_windows = []
        self.model = model
        self.side_panel = None
        self.canvas = None

    @close_other_windows
    def dialog_add_point(self):
        return ShowPointEditor(self.add_point)

    @close_other_windows
    def dialog_delete_point(self):
        max_index = len(self.get_points()) - 1
        return AskPointIndex(self.remove_point, max_index)

    @close_other_windows
    def dialog_edit_point(self):
        def show_editor(index):
            initial_point = self.fetch_point(index)
            return ShowPointEditor(lambda p: self.edit_point(index, p), initial_point)

        max_index = len(self.get_points()) - 1
        return AskPointIndex(show_editor, max_index)

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
        return self.model.get("points")

    def set_points(self, value):
        self.model.set("points", value)

    def set_side_panel(self, side_panel):
        self.side_panel = side_panel

    def set_canvas(self, canvas):
        self.canvas = canvas

    def try_solve(self):
        try:
            self.solve()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_task(self):
        task = "На плоскости дано множество точек.\n"
        task += "Найти такой треугольник с вершинами в этих точках,\n"
        task += "для которого разность площадей описанного и вписанного кругов максимальны\n"
        messagebox.showinfo("Task", task)

    def solve(self):
        points = self.get_points()
        if len(points) < 3:
            raise ValueError("Provide at least 3 distinct points!")

        if not has_any_triangles(points):
            raise ValueError("No triangles were found in your input!")
        triangle = solution.triangle_with_max_circle_area_difference(points)

        indices = list(map(self.get_points().index, triangle))

        triangle_str = ""
        for i in range(3):
            triangle_str += f"{triangle[i]} index={indices[i]}\n"

        difference = solution.area_difference(triangle)
        messagebox.showinfo(
            "Info",
            f"Answer is the triangle:\n{triangle_str}With circle area difference: {difference}",
        )
        self.render(triangle)

    def render(self, triangle):
        shapes = solution.get_shape_composition(triangle)

        # point indices
        indices = list(map(self.get_points().index, triangle))

        shapes["triangle"].point_names = {
            "a": indices[0],
            "b": indices[1],
            "c": indices[2],
        }
        self.canvas.draw_shapes(shapes)
