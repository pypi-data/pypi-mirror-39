class Layer(object):
    """
    基层
    """

    __slots__ = ('prelayer', 'nextlayer', 'feedin', 'feedout', 'backin', 'backout')

    # 基层的参数
    def __init__(self):

        self.prelayer = None
        self.nextlayer = None

        self.feedin = None
        self.feedout = None

        self.backin = None
        self.backout = None

    def feedforward(self):
        pass

    def backpropagation(self):
        pass

    def init(self):
        pass
