from dataclasses import dataclass

@dataclass
class Circle:
    x_0: float
    y_0: float
    radius: float

    def render(self, qp, transformation):
        pass

class Parabola:
    c: float
    d: float
