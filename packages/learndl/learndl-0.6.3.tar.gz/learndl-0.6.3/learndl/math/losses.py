import numpy as np


def mse(a, y, der=False):
    if not der:
        return 0.5 * (y - a) ** 2
    else:
        return -(y - a)


def binary_crossentropy(a, y, der=False):
    if not der:
        return -(y * np.log(a + 1e-08) + (1 - y) * np.log(1 - a + 1e-08))
    else:
        return (a - y) / (a * (1 - a) + 1e-08)


def categorical_crossentropy(a, y, der=False):
    if not der:
        return -y * np.log(a + 1e-08)
    else:
        return - y / (a + 1e-08)


losses = {
    'mse': mse,
    'binary_crossentropy': binary_crossentropy,
    'categorical_crossentropy': categorical_crossentropy
}
