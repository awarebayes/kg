import tkinter as tk
from view import SidePanelView, CanvasView
from model import Model
from controller import Controller


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.controller = Controller(self.model)

        self.side_panel = SidePanelView(self, self.controller)
        self.canvas = CanvasView(self, self.controller)

        self.side_panel.pack(side=tk.LEFT, expand=True, fill="both")
        self.canvas.pack(side=tk.LEFT)

        self.model.add_callback("points", self.side_panel.reformat_table)


if __name__ == "__main__":
    app = App()
    app.mainloop()
