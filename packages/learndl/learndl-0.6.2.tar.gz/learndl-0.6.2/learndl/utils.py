import numpy as np


def split(x, y, percent, shuffle_first=True):
    m = x.shape[0]
    if m * percent < 1:
        boundary = m - 1
    else:
        boundary = m - int(m * percent)

    if shuffle_first:
        x, y = shuffle(x, y)

    train_x = x[:boundary]
    train_y = y[:boundary]
    test_x = x[boundary:]
    test_y = y[boundary:]

    return train_x, test_x, train_y, test_y


def shuffle(x, y):
    data = np.hstack([x, y])
    np.random.shuffle(data)
    x_shuffled = data[:, :x.shape[1]]
    y_shuffled = data[:, -y.shape[1]:]

    return x_shuffled, y_shuffled


def one_hot(y, class_num):
    new = np.zeros((y.shape[0], class_num))
    for index, line in enumerate(new):
        line[y[index, 0]] = 1

    return new


def only_class(a):
    if a.shape[0] == 1:
        t = np.where(a > 0.5, 1, 0)
    else:
        t = np.where(a == a.max(0), 1, 0)

    return t
