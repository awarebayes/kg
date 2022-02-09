from tkinter import scrolledtext, messagebox
from prettytable import PrettyTable
import tkinter as tk


class SidePanelView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.add_button = tk.Button(self, text="Add point", command=controller.dialog_add_point)
        self.calculate_button = tk.Button(self, text="Calculate", command=controller.dialog_add_point)

        self.edit_button = tk.Button(self, text="Edit point", command=controller.dialog_edit_point)
        self.delete_button = tk.Button(self, text="Delete point", command=controller.dialog_delete_point)
        self.clear_button = tk.Button(self, text="Delete all points", command=controller.delete_all_points)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45,
                                                   height=50, font=("Times New Roman", 14))
        self.text_area.config(state=tk.DISABLED)

        self.add_button.grid(row=0, column=0)
        self.calculate_button.grid(row=0, column=1)
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
                table.add_row([i, point.x, point.y])
            string = table.get_string()
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, string)
        self.text_area.config(state=tk.DISABLED)


class CanvasView(tk.Frame):
    def __init__(self, parent, controller):
        super(CanvasView, self).__init__(parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, bg="black", height=800, width=800)
        self.canvas.pack()
