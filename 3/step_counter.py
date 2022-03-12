class StepCounter:
    def __init__(self):
        self.steps = 0
        self.y_saved = None
        self.x_saved = None

    def count_step(self, x, y, intensity=0):
        if y != self.y_saved and x != self.x_saved:
            self.steps += 1
        self.y_saved = y
        self.x_saved = x


class WuStepCounter(StepCounter):
    def __init__(self):
        super(WuStepCounter, self).__init__()
        self.calls = 0

    def count_step(self, x, y, intensity=0):
        if self.calls % 2 == 0:
            super().count_step(x, y, intensity)
        self.calls += 1
