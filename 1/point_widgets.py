import tkinter as tk
from abc import ABC
from dataclasses import dataclass
from tkinter import messagebox
from typing import Tuple, Optional, Callable, Any


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


class ToplevelWidget(tk.Toplevel, ABC):
    def __init__(self, callback: Callable, initial: Optional = None):
        super().__init__()
        self.callback = callback
        self.protocol("WM_DELETE_WINDOW", self.ask_should_continue)
        self.set_active()

    def ask_should_continue(self, error_message=None):
        if error_message is None:
            error_message = ""
        error_message += "Do you want to continue?"
        should_continue = messagebox.askyesno("Answer, please", error_message)
        if not should_continue:
            self.destroy()
            self.update()
        self.set_active()

    def get_value(self) -> any:
        pass

    def on_proceed(self):
        try:
            value = self.get_value()
            self.callback(value)
            self.destroy()
            self.update()
        except ValueError as e:
            error_message = str(e)
            self.ask_should_continue(error_message)

    def set_active(self):
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()


class ShowPointEditor(ToplevelWidget):
    def __init__(self, callback, initial=None):
        super().__init__(callback)

        if initial is None:
            initial = Point(0.0, 0.0)

        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.x_var.set(str(initial.x))
        self.y_var.set(str(initial.y))
        self.label_var = tk.StringVar()

        self.x_label = tk.Label(self, text="x:", font=14)
        self.x_input = tk.Entry(self, textvariable=self.x_var, width=16, font=14)

        self.y_label = tk.Label(self, text="y:", font=14)
        self.y_input = tk.Entry(self, textvariable=self.y_var, width=16, font=14)

        self.finish_button = tk.Button(self, text="Finish", command=self.on_proceed)

        self.x_label.grid(row=0, column=0)
        self.x_input.grid(row=0, column=1)

        self.y_label.grid(row=1, column=0)
        self.y_input.grid(row=1, column=1)

        self.finish_button.grid(row=2, column=0, columnspan=2)

    def get_value(self):
        x_var = self.x_var.get()
        y_var = self.y_var.get()
        try:
            x = float(x_var)
            y = float(y_var)
            return Point(x, y)
        except ValueError:
            error_message = "Error: your point is invalid\n"
            if not is_float(x_var):
                error_message += f" X-component should be float, got: {x_var}\n"
            if not is_float(y_var):
                error_message += f" Y-component should be float, got: {y_var}\n"
            raise ValueError(error_message)


class AskPointIndex(ToplevelWidget):
    def __init__(self, callback: Callable, max_index: int):
        super().__init__(callback)

        if max_index == -1:
            self.destroy()
            self.update()
            messagebox.showerror("Error", "No points were added!")

        self.callback = callback
        self.index_var = tk.StringVar()
        self.index_var.set("0")
        self.max_index = max_index

        self.index_label = tk.Label(
            self, text=f"Index of point[0...{max_index}]: ", font=14
        )
        self.index_entry = tk.Entry(
            self, textvariable=self.index_var, width=16, font=14
        )

        self.proceed_button = tk.Button(self, text="Proceed", command=self.on_proceed)

        self.index_label.grid(row=0, column=0)
        self.index_entry.grid(row=0, column=1)
        self.proceed_button.grid(row=1, column=0, columnspan=2)

    def get_value(self):
        x_var = self.index_var.get()
        try:
            x = float(x_var)
        except ValueError:
            raise ValueError("Your value is not numeric\n")
        if not x.is_integer():
            raise ValueError("Integer value expected\n")
        x = int(x)
        if not (0 <= x <= self.max_index):
            raise ValueError(f"Your integer should be in [0...{self.max_index}]\n")
        return x
