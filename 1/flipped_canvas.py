from tkinter import Canvas


class FlippedCanvas(Canvas):

    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, width=width, height=height, *args, **kwargs)
        self.width = width
        self.height = height

    def create_line(self, x0: float, y0: float, x1: float, y1: float, *args, **kwargs):
        y0 = self.height - y0
        y1 = self.height - y1
        return super().create_line(x0, y0, x1, y1, *args, **kwargs)

    def create_oval(self, x0: float, y0: float, x1: float, y1: float, *args, **kwargs):
        y0 = self.height - y0
        y1 = self.height - y1
        return super().create_oval(x0, y0, x1, y1, *args, **kwargs)

    def create_rectangle(self, x0: float, y0: float, x1: float, y1: float, *args, **kwargs):
        y0 = self.height - y0
        y1 = self.height - y1
        return super().create_rectangle(x0, y0, x1, y1, *args, **kwargs)

    def create_text(self, x: float, y: float, *args, **kwargs):
        y = self.height - y
        return super().create_text(x, y, *args, **kwargs)
