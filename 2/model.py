import copy
from dataclasses import dataclass
from typing import Any, List

import numpy as np
from transforms import (
    BaseTransform,
    ScaleAroundPoint,
    RotateAroundPoint,
    TranslateTransform,
)


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
            "trans_x": ObservableFloat(0, -0.5, 0.5),
            "trans_y": ObservableFloat(0, -0.5, 0.5),
            "rotate": ObservableFloat(0, -180, 180),
            "scale_x": ObservableFloat(1, low=0.01, high=5),
            "scale_y": ObservableFloat(1, low=0.01, high=5),
            "sr_center_x": ObservableFloat(0.5, low=0.01, high=1),
            "sr_center_y": ObservableFloat(0.5, low=0.01, high=1),
            "a": ObservableFloat(0.5, low=0.01, high=1),
            "b": ObservableFloat(0.5, low=0.01, high=1),
            "c": ObservableFloat(0.5, low=0.01, high=1),
            "d": ObservableFloat(0.5, low=0.01, high=1),
            "r": ObservableFloat(0.1, low=0.01, high=1),
            "transform_array": Observable(list()),
            "show_base_figures": Observable(False),
        }

        self.transformation_fields = [
            "trans_x",
            "trans_y",
            "rotate",
            "scale_x",
            "scale_y",
            "sr_center_x",
            "sr_center_y",
        ]
        self.parameter_fields = ["a", "b", "c", "d", "r", "show_base_figures"]

    def add_callback(self, field, callback):
        self.observables[field].add_callback(callback)

    def get(self, field):
        return self.observables[field].get()

    def set(self, field, value):
        self.observables[field].set(value)

    def get_parameters(self):
        return Parameters(**{field: self.get(field) for field in self.parameter_fields})

    def get_state(self):
        return {k: self.get(k) for k in self.observables.keys()}


@dataclass
class HistoryRecord:
    field: str
    old_value: Any
    new_value: Any


class ModelWithHistory(Model):
    def __init__(self, record_fields=None):
        super().__init__()
        if record_fields is None:
            record_fields = []
        self.history: List[HistoryRecord] = []
        self.future_history: List[HistoryRecord] = []
        self.observables["can_go_forward"] = Observable(False)
        self.record_fields = record_fields
        self.muted = False

    def set(self, field, value):
        if field in self.record_fields and not self.muted:
            old_value = self.get(field)
            self.history_log(field, old_value, value)
        super().set(field, value)

    def history_back(self):
        if self.history:
            last_action = self.history.pop()
            super().set(last_action.field, last_action.old_value)
            self.future_history.append(last_action)
            super().set("can_go_forward", True)

    def history_forward(self):
        assert self.get("can_go_forward")
        if self.future_history:
            last_action = self.future_history.pop()
            super().set(last_action.field, last_action.new_value)
            self.history.append(last_action)
            if not self.future_history:
                super().set("can_go_forward", False)

    def history_log(self, field, old_value, new_value):
        self.history.append(HistoryRecord(field, old_value, new_value))
        self.future_history = []

    def register_transformation(self, kind):
        transform = None
        if kind == "translate":
            transform = TranslateTransform(
                trans_x=self.get("trans_x"), trans_y=self.get("trans_y")
            )
        elif kind == "scale":
            transform = ScaleAroundPoint(
                point_x=self.get("sr_center_x"),
                point_y=self.get("sr_center_y"),
                sx=self.get("scale_x"),
                sy=self.get("scale_y"),
            )
        elif kind == "rotate":
            transform = RotateAroundPoint(
                point_x=self.get("sr_center_x"),
                point_y=self.get("sr_center_y"),
                deg=self.get("rotate"),
            )
        old_array = self.get("transform_array")
        new_array = copy.copy(old_array)
        new_array.append(transform)
        self.set("transform_array", new_array)
        self.history_log("transform_array", old_array, new_array)
