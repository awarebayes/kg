from dataclasses import dataclass


@dataclass
class Transformation:
    trans_x: float
    trans_y: float
    scale: float
    rotation: float

    def rescale(self, width, height):
        self.trans_x *= width
        self.trans_y *= height


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


class Model:
    def __init__(self):
        self.observables = {
            "trans_x": Observable(0),
            "trans_y": Observable(0),
            "rotate": Observable(0),
            "scale": Observable(1),
            "show_sliders": Observable(True),
            "show_base_figures": Observable(False),
        }

        self.transformation_fields = ['trans_x', 'trans_y', 'rotate', 'scale']

    def add_callback(self, field, callback):
        self.observables[field].add_callback(callback)

    def get(self, field):
        return self.observables[field].get()

    def set(self, field, value):
        self.observables[field].set(value)

    def get_transformation(self):
        return Transformation(
            **{field: self.get(field) for field in self.transformation_fields}
        )