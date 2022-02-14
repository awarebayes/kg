from dataclasses import dataclass


@dataclass
class Transformations:
    trans_x: float
    trans_y: float
    scale: float
    rotate: float

    def rescale(self, dim):
        self.trans_x *= dim
        self.trans_y *= dim

@dataclass
class Parameters:
    a: float
    b: float
    c: float
    d: float
    r: float
    show_base_figures: bool

    def rescale(self, dim):
        self.a *= dim
        self.b *= dim
        self.c *= dim
        self.d *= dim
        self.r *= dim


class Observable:
    def __init__(self, value):
        self._value = value
        self._callbacks = []

    def notify(self):
        for cb in self._callbacks:
            cb(self._value)

    def set(self, value):
        self._value = value
        self.notify()

    def get(self):
        return self._value

    def add_callback(self, cb):
        self._callbacks.append(cb)


class ObservableFloat(Observable):
    def __init__(self, value, low, high):
        super(ObservableFloat, self).__init__(value)
        self.low = low
        self.high = high

    def get_norm(self):
        return (self.get() - self.low) / (self.high - self.low)

    def set(self, value):
        assert self.low <= value <= self.high
        super().set(value)

    def notify(self):
        for cb in self._callbacks:
            cb(self.get())

    def set_from_slider(self, value):
        assert 0 <= value <= 99
        norm = value / 100
        norm = round(norm, 2)
        new_value = norm * (self.high - self.low) + self.low
        self.set(new_value)


class Model:
    def __init__(self):
        self.observables = {
            "trans_x": ObservableFloat(0, 0.0, 1.0),
            "trans_y": ObservableFloat(0, 0.0, 1.0),
            "rotate": ObservableFloat(0, -180, 180),
            "scale": ObservableFloat(1, 0.1, 5),
            "a": ObservableFloat(0.01, 0.01, 1),
            "b": ObservableFloat(0.01, 0.01, 1),
            "c": ObservableFloat(0.01, 0.01, 1),
            "d": ObservableFloat(0.01, 0.01, 1),
            "r": ObservableFloat(0.01, 0.01, 1),
            "show_base_figures": Observable(False),
        }

        self.transformation_fields = ["trans_x", "trans_y", "rotate", "scale"]
        self.parameter_fields = ["a", "b", "c", "d", "r", "show_base_figures"]

    def add_callback(self, field, callback):
        self.observables[field].add_callback(callback)

    def get(self, field):
        return self.observables[field].get()

    def set(self, field, value):
        self.observables[field].set(value)

    def get_transformations(self):
        return Transformations(
            **{field: self.get(field) for field in self.transformation_fields}
        )

    def get_parameters(self):
        return Parameters(
            **{field: self.get(field) for field in self.parameter_fields}
        )
