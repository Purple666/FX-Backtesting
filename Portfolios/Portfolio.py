from abc import ABCMeta, abstractmethod


class Portfolio(object):
    __metaclass__ = ABCMeta

    def __init__(self, init_capital):
        self.init_capital = init_capital

    @abstractmethod
    def order(self):
        raise NotImplementedError('Should implement order() method')

    @abstractmethod
    def update(self):
        raise NotImplementedError('Should implement update() method')
