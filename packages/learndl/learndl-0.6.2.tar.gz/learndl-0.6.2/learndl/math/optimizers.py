import numpy as np


class SGD(object):

    def __init__(self, alpha=0.01, decay=0.0):
        self.alpha = alpha
        self.decay = decay

    def update(self, layer, epoch):
        # 更新
        _alpha = 1 / (1 + self.decay * epoch) * self.alpha
        layer.w -= _alpha * layer.dw
        layer.b -= _alpha * layer.db


class Momentum(object):

    def __init__(self, alpha=0.001, beta=0.9, decay=0.0):
        self.alpha = alpha
        self.beta = beta
        self.decay = decay

    def update(self, layer, epoch):
        _alpha = 1 / (1 + self.decay * epoch) * self.alpha
        layer.vdw = self.beta * layer.vdw + (1 - self.beta) * layer.dw
        layer.vdb = self.beta * layer.vdb + (1 - self.beta) * layer.db

        # 更新
        layer.w -= _alpha * layer.vdw
        layer.b -= _alpha * layer.vdb


class RMSprop(object):

    def __init__(self, alpha=0.001, beta=0.999, epsilon=1e-08, decay=0.0):
        self.alpha = alpha
        self.beta = beta
        self.epsilon = epsilon
        self.decay = decay

    def update(self, layer, epoch):
        _alpha = 1 / (1 + self.decay * epoch) * self.alpha
        layer.sdw = self.beta * layer.sdw + (1 - self.beta) * (layer.dw ** 2)
        layer.sdb = self.beta * layer.sdb + (1 - self.beta) * (layer.db ** 2)

        # 更新
        layer.w -= _alpha * (layer.dw / (np.sqrt(layer.sdw) + self.epsilon))
        layer.b -= _alpha * (layer.db / (np.sqrt(layer.sdb) + self.epsilon))


class Adam(object):

    def __init__(self, alpha=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, decay=0.0):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.decay = decay
        self.t = None

    def update(self, layer, epoch):
        _alpha = 1 / (1 + self.decay * epoch) * self.alpha
        layer.vdw = self.beta1 * layer.vdw + (1 - self.beta1) * layer.dw
        layer.vdb = self.beta1 * layer.vdb + (1 - self.beta1) * layer.db
        layer.sdw = self.beta2 * layer.sdw + (1 - self.beta2) * (layer.dw ** 2)
        layer.sdb = self.beta2 * layer.sdb + (1 - self.beta2) * (layer.db ** 2)

        # 偏差修正
        vcdw = layer.vdw / (1 - self.beta1 ** self.t)
        vcdb = layer.vdb / (1 - self.beta1 ** self.t)
        scdw = layer.sdw / (1 - self.beta2 ** self.t)
        scdb = layer.sdb / (1 - self.beta2 ** self.t)

        # 更新
        layer.w -= _alpha * (vcdw / (np.sqrt(scdw) + self.epsilon))
        layer.b -= _alpha * (vcdb / (np.sqrt(scdb) + self.epsilon))


# 策略字典
optimizers = {
    'sgd': SGD,
    'momentum': Momentum,
    'rmsprop': RMSprop,
    'adam': Adam
}
