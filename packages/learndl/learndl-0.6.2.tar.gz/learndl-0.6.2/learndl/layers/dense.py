import numpy as np
from . import Layer
from ..math.activations import activations


class Dense(Layer):

    __slots__ = ('units', 'w', 'b', 'z', 'activation',
                 'dz', 'dw', 'db', 'vdw', 'vdb', 'sdw', 'sdb')

    # 全连接层的参数
    def __init__(self, units, s):

        # 层的参数
        super(Dense, self).__init__()
        self.units = units

        # 正向传播参数
        self.w = None
        self.b = None
        self.z = None
        self.activation = s

        # 反向传播参数
        self.dz = None

        # optimizer
        self.vdw = None
        self.vdb = None
        self.sdw = None
        self.sdb = None
        self.dw = None
        self.db = None

    # 正向传播
    def feedforward(self) -> None:

        # 向前一层要值
        self.feedin = self.prelayer.feedout

        # feedforward
        self.z = self.w @ self.feedin + self.b
        self.feedout = activations[self.activation](self.z)

    # 反向传播
    def backpropagation(self) -> None:

        # 向后一层要值
        self.backin = self.nextlayer.backout

        # backpropagation
        dadz = activations[self.activation](self.z, der=True)

        if self.activation == 'softmax':
            n = self.backin.shape[0]
            m = self.backin.shape[1]
            # 3d tensor multiply: a和每一个z都有关，所以用点乘
            self.dz = (dadz @ self.backin.reshape(m, n, 1)).reshape(m, n).T
        else:
            self.dz = self.backin * dadz

        self.backout = self.w.T @ self.dz

        self.dw = self.dz @ self.feedin.T / self.feedin.shape[1]
        self.db = self.dz.mean(1, keepdims=True)

    # 初始化权重（weight）&偏置（bias）
    def init(self) -> None:

        self.w = np.random.randn(self.units, self.prelayer.units) * 0.01
        self.b = np.zeros((self.units, 1))

        self.vdw = np.zeros_like(self.w)
        self.vdb = np.zeros_like(self.b)

        self.sdw = np.zeros_like(self.w)
        self.sdb = np.zeros_like(self.b)
