from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


class Observable:
    def __init__(self, value):
        self._value = value
        self._callbacks = []

    def notify(self):
        for cb in self._callbacks:
            cb()

    def set(self, value):
        self._value = value
        self.notify()

    def get(self):
        return self._value

    def add_callback(self, cb):
        self._callbacks.append(cb)


class Model:
    def __init__(self):
        self.observables = {"points": Observable(list())}

    def add_callback(self, field, callback):
        self.observables[field].add_callback(callback)

    def get(self, field):
        return self.observables[field].get()

    def set(self, field, value):
        self.observables[field].set(value)
