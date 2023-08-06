import numpy as np


def linear(x, der=False):
    if not der:
        return x
    else:
        return 1


def sigmoid(x, der=False):
    if not der:
        return 1 / (1 + np.exp(-x))
    else:
        return sigmoid(x) * (1 - sigmoid(x))


def tanh(x, der=False):
    if not der:
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
    else:
        return 1 - tanh(x) ** 2


def relu(x, der=False):
    if not der:
        return np.max(0, x)
    else:
        return 1 if x > 0 else 0


def leaky_relu(x, der=False):
    if not der:
        return np.max(0.01*x, x)
    else:
        return 1 if x > 0 else 0.01


def softmax(x, der=False):
    if not der:
        t = np.exp(x)
        return t / t.sum(0)
    else:
        a = softmax(x)
        n = x.shape[0]
        m = x.shape[1]
        res = np.empty((m, n, n))
        for index in range(m):
            for x in range(n):
                for y in range(n):
                    if x == y:
                        res[index, x, y] = a[x, index] * (1 - a[x, index])
                    else:
                        res[index, x, y] = -a[x, index] * a[y, index]
        return res


activations = {
    'linear': linear,
    'sigmoid': sigmoid,
    'tanh': tanh,
    'relu': relu,
    'leaky_relu': leaky_relu,
    'softmax': softmax
}
