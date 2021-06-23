import numpy as np


def range_from_series(ser):
    return extend_range((ser.min(), ser.max()))


def extend_range(r):
    return r[0] * (1 - 0.1 * np.sign(r[0])), r[1] * (1 + 0.2 * np.sign(r[1]))