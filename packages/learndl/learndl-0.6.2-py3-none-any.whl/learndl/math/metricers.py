import numpy as np
from .. import utils


def accuracy(a, y):
    t = utils.only_class(a)

    right = np.count_nonzero(t == y) / t.shape[0]
    total = t.shape[1]

    return right / total


def error_rate(a, y):
    return 1 - accuracy(a, y)


def precision(a, y):
    t = utils.only_class(a)

    p = np.empty(t.shape[0])
    for i in range(t.shape[0]):
        numerator = np.count_nonzero(y[i][t[i] == 1] == 1)
        denominator = np.count_nonzero(t[i] == 1) + 1e-8
        p[i] = numerator / denominator

    return p


def recall(a, y):
    t = utils.only_class(a)

    r = np.empty(t.shape[0])
    for i in range(t.shape[0]):
        numerator = np.count_nonzero(t[i][y[i] == 1] == 1)
        denominator = np.count_nonzero(y[i] == 1) + 1e-8
        r[i] = numerator / denominator

    return r


def f1(a, y):
    p = precision(a, y)
    r = recall(a, y)
    f = 2 * p * r / (p + r + 1e-08)

    return f


# 策略字典
metricers = {
    'acc': accuracy,
    'err': error_rate,
    'precision': precision,
    'recall': recall,
    'f1': f1
}
