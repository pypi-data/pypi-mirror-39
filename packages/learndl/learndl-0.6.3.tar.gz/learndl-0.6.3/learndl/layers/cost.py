import sys
import pandas as pd
from .layer import Layer
from ..math.losses import losses
from ..math.metricers import metricers


class Cost(Layer):

    __slots__ = ('loss', 'metrics', 'lossdict', 'metricsdict', 'process', 'display', 'df')

    # 损失层的参数
    def __init__(self, loss, metrics=None, display=False):

        super(Cost, self).__init__()

        # 损失函数
        self.loss = loss  # （string）损失函数名
        self.lossdict = {'train': [], 'val': [], 'test': []}

        # 性能度量
        self.metrics = metrics
        self.metricsdict = {
            'acc': {'train': [], 'val': [], 'test': []},
            'err': {'train': [], 'val': [], 'test': []},
            'precision': {'train': [], 'val': [], 'test': []},
            'recall': {'train': [], 'val': [], 'test': []},
            'f1': {'train': [], 'val': [], 'test': []}
        }

        # 性能度量
        self.metrics = []
        if isinstance(metrics, list):
            self.metrics.extend(metrics)
        elif metrics is None:
            pass
        else:
            raise TypeError('metric needs to be a list of string')

        # 是否输出metrics
        self.display = display
        self.df = {
            'train': pd.DataFrame(),
            'val': pd.DataFrame(),
            'test': pd.DataFrame()
        }

    # 正向传播
    def feedforward(self) -> None:
        # 向前一层要值
        self.feedin = self.prelayer.feedout

        # 根据选定的损失函数计算误差矩阵
        self.feedout = losses[self.loss](self.feedin, self.backin)

        # 计算、保存并打印损失
        self.lossdict[self.process].append(self.feedout.sum(0, keepdims=True).mean())
        print('loss: {loss:>6.3f}'.format(loss=self.lossdict[self.process][-1]), end=' ')
        sys.stdout.flush()

        # 计算、保存并打印性能度量标准
        if self.metrics:
            for mt in self.metrics:
                # 计算、保存
                res = metricers[mt](self.feedin, self.backin)
                self.metricsdict[mt][self.process].append(res)

                if mt == 'acc' or mt == 'err':
                    print('- {mt}: {res:>6.4f}'.format(mt=mt, res=res), end=' ')
                    sys.stdout.flush()
                else:
                    self.df[self.process][mt] = res

            if (self.display is True) or (self.process == 'test'):
                print('\n', self.df[self.process].round(4))
                sys.stdout.flush()

    # 反向传播
    def backpropagation(self) -> None:

        # 根据选定的损失函数计算误差导数
        self.backout = losses[self.loss](self.feedin, self.backin, der=True)
