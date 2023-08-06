import sys
import numpy as np
from .layers import Cost
from .math.optimizers import optimizers
from . import utils
from .decorators import log


class NeuralNetwork(object):

    __slots__ = ('layers', 'optimizer')

    # 构建仅含有层容器的空模型
    def __init__(self):

        self.layers = []
        self.optimizer = None

    # 将层添加进模型中，并连接
    def add(self, layer) -> None:
        # add
        self.layers.append(layer)
        
        # link
        if len(self.layers) > 1:
            self.layers[-1].prelayer = self.layers[-2]
            self.layers[-2].nextlayer = self.layers[-1]

        # init
        layer.init()

    # 设置损失函数和性能度量标准
    def set(self, loss, optimizer='sgd', metrics=None, display=False):
        layer = Cost(loss, metrics, display)
        self.add(layer)

        # 优化器
        if isinstance(optimizer, str):
            self.optimizer = optimizers[optimizer]()
        else:
            self.optimizer = optimizer

    # 训练
    @ log('Training')
    def train(self, x, y, epochs=3000, batch_size=64, validation=0.0, shuffle=True) -> None:
        # shuffle
        if shuffle:
            x, y = utils.shuffle(x, y)

        # training
        iterations = 0  # for adam
        for epoch in range(epochs):
            print('epoch {current:>3d}/{all:<d}'.format(current=epoch+1, all=epochs))

            # per batch
            batchs = int(np.ceil(x.shape[0] / batch_size))
            for batch in range(batchs):

                # for adam algorithm
                iterations += 1
                if isinstance(self.optimizer, optimizers['adam']):
                    self.optimizer.t = iterations  # feed t into adam

                # 计算batch
                start = batch * batch_size
                end = min((batch+1)*batch_size, x.shape[0])

                # train / validation
                x_train, x_val, y_train, y_val = \
                    utils.split(x[start: end], y[start: end], validation, False)

                # 传入数据集
                self.layers[0].feedin = x_train.T
                self.layers[-1].backin = y_train.T
                self.layers[-1].process = 'train'

                # 打印batch
                print('\r' + '{current:>2d}/{all:<2d} '.format(current=batch + 1, all=batchs), end='')
                # 进度条
                already = int((batch+1) / batchs * 25)
                print('▇' * already + ' ' * (25 - already), end=' ')
                sys.stdout.flush()

                # 正向传播
                for layer in self.layers:
                    layer.feedforward()

                # 反向传播
                self.layers[-1].backpropagation()
                for layer in self.layers[-2:0:-1]:
                    layer.backpropagation()
                    self.optimizer.update(layer, epoch)

                # 交叉验证
                if validation > 0:
                    self.layers[0].feedin = x_val.T
                    self.layers[-1].backin = y_val.T
                    self.layers[-1].process = 'val'

                    print(' {marker} {val} {marker} '.format(marker='-' * 9, val='validation'), end='')
                    for layer in self.layers:
                        layer.feedforward()

            print()  # 换行

    # 测试
    @ log('Testing')
    def test(self, x, y) -> None:
        self.layers[0].feedin = x.T
        self.layers[-1].backin = y.T
        self.layers[-1].process = 'test'

        # 正向传播
        for layer in self.layers:
            layer.feedforward()

        print()  # 换行

    # 预测
    @ log('Predicting')
    def predict(self, x, onlyclass=False) -> None:
        self.layers[0].feedin = x.T

        for layer in self.layers[:-1]:
            layer.feedforward()

        if not onlyclass:
            print('prediction:\n', self.layers[-2].feedout)
        else:
            a = self.layers[-1].feedout
            t = utils.only_class(a)
            print('prediction:\n', t)

    # 打印 metrics
    def scores(self, processes):
        layer = self.layers[-1]
        for process in processes:
            print('{marker} {pro:^7s} {marker}'.format(marker='*' * 10, pro=process.upper()))
            print('** LOSS: {loss:>17.3f} **'.format(loss=layer.lossdict[process][-1]))
            for mt in layer.metrics:
                if mt == 'acc' or mt == 'err':
                    print('** {name}: {mt:>18.4f} **'.format(name=mt.upper(), mt=layer.metricsdict[mt][process][-1]))

            if not layer.df[process].empty:
                print(layer.df[process].round(4))

            print('*' * 29, '\n')
