from tkinter import scrolledtext, messagebox
from prettytable import PrettyTable
import tkinter as tk
from shapes import ObjectComposition
from flipped_canvas import  FlippedCanvas


class SidePanelView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.add_button = tk.Button(
            self, text="Add point", command=controller.dialog_add_point, font=13
        )
        self.calculate_button = tk.Button(
            self, text="Calculate", command=controller.try_solve, font=13
        )

        self.task_button = tk.Button(
            self, text="Show task", command=controller.show_task, font=13
        )

        self.edit_button = tk.Button(
            self, text="Edit point", command=controller.dialog_edit_point, font=13
        )
        self.delete_button = tk.Button(
            self, text="Delete point", command=controller.dialog_delete_point, font=13
        )
        self.clear_button = tk.Button(
            self,
            text="Delete all points",
            command=controller.delete_all_points,
            font=13,
        )

        self.text_area = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=45, height=30, font=("Consolas", 14)
        )
        self.text_area.config(state=tk.DISABLED)

        self.add_button.grid(row=0, column=0)
        self.calculate_button.grid(row=0, column=1)
        self.task_button.grid(row=0, column=2)
        self.edit_button.grid(row=1, column=0)
        self.delete_button.grid(row=1, column=1)
        self.clear_button.grid(row=1, column=2)
        self.text_area.grid(row=2, column=0, columnspan=3)
        self.reformat_table()

    def reformat_table(self):
        points = self.controller.get_points()
        if not points:
            string = "No points no show yet, click `add_point`"
        else:
            table = PrettyTable()
            table.field_names = ["Idx", "X", "Y"]
            for i, point in enumerate(points):
                x_str = f"{point.x:.10g}"
                y_str = f"{point.y:.10g}"
                table.add_row([i, x_str, y_str])
            string = table.get_string()
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, string)
        self.text_area.config(state=tk.DISABLED)


class CanvasView(tk.Frame):
    def __init__(self, parent, controller, width, height):
        super(CanvasView, self).__init__(parent)
        self.controller = controller
        self.height = height
        self.width = width
        self.canvas = FlippedCanvas(self, bg="white", height=height, width=width)
        self.canvas.pack()
        self.canvas.update()

    def get_canvas_dim(self):
        return self.width, self.height

    def draw_shapes(self, shapes: ObjectComposition):
        self.canvas.delete("all")
        shapes.fit_to_canvas(self.get_canvas_dim())
        shapes['triangle'].draw(self.canvas, fill="red", width=2)
        shapes['in_circ'].draw(self.canvas, outline="blue", width=2)
        shapes['out_circ'].draw(self.canvas, outline="green", width=2)
