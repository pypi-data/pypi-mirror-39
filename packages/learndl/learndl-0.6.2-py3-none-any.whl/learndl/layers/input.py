from .layer import Layer


class Input(Layer):

    __slots__ = 'units'

    def __init__(self, units):

        super(Input, self).__init__()
        self.units = units

    def feedforward(self) -> None:

        self.feedout = self.feedin
