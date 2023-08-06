import numpy as np
from typing import Union


class Parameter:
    def __init__(self, x: float, is_const: bool):
        self.val = x
        self.is_const = is_const

    def __mul__(self, x):
        return self.val * x

    def __rmul__(self, x):
        return self.val * x

    def __add__(self, x):
        return self.val + x

    def __radd__(self, x):
        return self.val + x

    def __sub__(self, x):
        return self.val - x

    def __rsub__(self, x):
        return x - self.val

    def __truediv__(self, x):
        return self.val / x

    def __rtruediv__(self, x):
        return x / self.val

    def __neg__(self):
        return -self.val

    def __pow__(self, b):
        return self.val**b

    def __rpow__(self, b):
        return b**self.val
